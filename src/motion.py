#!/usr/bin/env python

import datetime
import sys
import time

# Camera Support
import cv2
import imutils
from picamera import PiCamera
from picamera.array import PiRGBArray

# PiOLED Support
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

class Display(object):
	def __init__(self):
		# Raspberry Pi pin configuration:
		self.RST = None     # on the PiOLED this pin isnt used
		# Note the following are only used with SPI:
		self.DC = 23
		self.SPI_PORT = 0
		self.SPI_DEVICE = 0

		self.disp = Adafruit_SSD1306.SSD1306_128_32(rst=self.RST)

		# Initialize library.
		self.disp.begin()

		self.disp.clear()
		self.disp.display()

		# Create blank image for drawing.
		# Make sure to create image with mode '1' for 1-bit color.
		self.width = self.disp.width
		self.height = self.disp.height
		self.image = Image.new('1', (self.width, self.height))

		# Get drawing object to draw on image.
		self.draw = ImageDraw.Draw(self.image)
		self.clear()

		# Load default font.
		self.font = ImageFont.load_default()

	def clear(self):
		# Draw a black filled box to clear the image.
		self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)

	def text(self, x, y, message):
		self.draw.text((x, y), message, font=self.font, fill=255)

	def display(self):
		self.disp.image(self.image)
		self.disp.display()


class MotionDetection(object):
	def __init__(self, w=320, h=240, framerate=10):
		self.w = w
		self.h = h
		self.cam = PiCamera()
		self.cam.resolution = tuple([self.w, self.h])
		self.framerate = framerate
		self.raw = PiRGBArray(self.cam, size=self.cam.resolution)
		self.avg = None
		self.n = 0
		self.startTime = None
		self.motion_callbacks = []
		self.nomotion_callbacks = []
		self.timestamp = None

	def grayscale(self):
		self.gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
		self.gray = cv2.GaussianBlur(self.gray, (21, 21), 0)

	def compute_delta(self):
		if self.avg is None:
			self.avg = self.gray.copy().astype("float")
			self.raw.truncate(0)
			self.delta = None
		cv2.accumulateWeighted(self.gray, self.avg, 0.5)
		self.delta = cv2.absdiff(self.gray, cv2.convertScaleAbs(self.avg))

	def detect_contours(self):
		# threshold the delta image, dilate the thresholded image to fill
		# in holes, then find contours on thresholded image
		thresh = cv2.threshold(self.delta, 5, 255, cv2.THRESH_BINARY)[1]
		thresh = cv2.dilate(thresh, None, iterations=2)
		(_, self.cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	def detect_motion(self, boundingBox=False):
		self.n += 1
		motionDetected = False
		# loop over the contours
		for c in self.cnts:
			# if the contour is too small, ignore it
			if cv2.contourArea(c) < 5000:
				continue

			# compute the bounding box for the contour, draw it on the frame,
			# and update the text
			(x, y, w, h) = cv2.boundingRect(c)
			if boundingBox:
				cv2.rectangle(self.frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
			motionDetected = True

		if self.n < 10:
			return False

		return motionDetected

	def save(self, frame, filename):
		cv2.imwrite(filename, frame)

	def save_debug_images(self):
		self.save(self.frame, 'frame.png')
		self.save(self.gray,  'gray.png')
		self.save(self.delta, 'delta.png')

	def set_motion_callback(self, cb):
		self.motion_callbacks.append(cb)

	def set_nomotion_callback(self, cb):
		self.nomotion_callbacks.append(cb)

	def get_rate(self):
		if self.timestamp is None:
			return ''
		if self.starttime is None:
			return ''
		if self.n == 0:
			return ''
		return self.n / (self.timestamp - self.starttime).total_seconds()

	def run(self):
		self.starttime = datetime.datetime.now()
		for f in self.cam.capture_continuous(self.raw, format='bgr', use_video_port=True):
			self.timestamp = datetime.datetime.now()

			self.frame = f.array
			self.grayscale()
			self.compute_delta()

			if self.delta is not None:
				self.detect_contours()
				motion = self.detect_motion(boundingBox=True)
				if motion:
					for cb in self.motion_callbacks:
						cb()
				else:
					for cb in self.nomotion_callbacks:
						cb()

			self.raw.truncate(0)

def motion_detected():
	global g_motion
	if g_motion == False:
		oled.text(0, 10, "    ** Motion ** ")
		oled.display()
		g_motion = True
	print(md.get_rate())
	md.save_debug_images()
	sys.exit()

def no_motion_detected():
	global g_motion
	if g_motion == True:
		oled.clear()
		oled.display()
		g_motion = False
	print(md.get_rate())


oled = Display()
md = MotionDetection()
g_motion = False
md.set_motion_callback(motion_detected)
md.set_nomotion_callback(no_motion_detected)
md.run()
