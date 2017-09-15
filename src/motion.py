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

oled = Display()


rez = [320,240]
cam = PiCamera()
cam.resolution = tuple(rez)
cam.framerate = 5
raw = PiRGBArray(cam, size=tuple(rez))

avg = None

lastTime = None

n = 0
for f in cam.capture_continuous(raw, format='bgr', use_video_port=True):
	n += 1
	motion = False
	frame = f.array
	timestamp = datetime.datetime.now()
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (21, 21), 0)

	if avg is None:
		avg = gray.copy().astype("float")
		raw.truncate(0)
		continue

	cv2.accumulateWeighted(gray, avg, 0.5)
	delta = cv2.absdiff(gray, cv2.convertScaleAbs(avg))

	# threshold the delta image, dilate the thresholded image to fill
	# in holes, then find contours on thresholded image
	thresh = cv2.threshold(delta, 5, 255, cv2.THRESH_BINARY)[1]
	thresh = cv2.dilate(thresh, None, iterations=2)
	(_, cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	# loop over the contours
	for c in cnts:
		# if the contour is too small, ignore it
		if cv2.contourArea(c) < 5000:
			continue

		# compute the bounding box for the contour, draw it on the frame,
		# and update the text
		(x, y, w, h) = cv2.boundingRect(c)
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
		motion = True

	if motion:
		## draw the text and timestamp on the frame
		ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
		##cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
		##	cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
		#cv2.putText(frame, ts, (10, frame.shape[0] - 10),
		#	cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

		#if n > 10:
		#	cv2.imwrite("avg.png", avg)
		#	cv2.imwrite("gray.png", gray)
		#	cv2.imwrite("pic.png", frame)
		#	sys.exit()
		oled.text(0, 10, "    ** Motion ** ")
	else:
		oled.clear()

	oled.display()


	raw.truncate(0)
	if n % 10 == 0:
		if lastTime is not None:
			dt = time.time() - lastTime
			# print 10. / dt
		lastTime = time.time()
