# rpi-tf
Raspberry Pi 3 B with OpenCV and Tensorflow

## Motivation

Our "headless" Pi will run a Python script automatically launched at boot time.
This script will monitor the camera and use OpenCV to detect motion.  When
motion is detected, it will perform face detection on the captured frame, again
using OpenCV.  Detected faces will be cropped from the overall captured frame
and will be saved to a USB flash drive as unlabeled data for training a neural
network.

When the script detects the insertion of a second USB flash drive, it will
shutdown the Pi gracefully so the full drive can be safely removed.  Once
powered again, it will continue to detect motion and save unlabeled data to the
new drive.

Off-line, the captured faces will be manually labeled and used to design and
train a neural network to identify key individuals.  The trained neural network
will eventually run on the Pi itself and play audible alert messages to the
identified individuals.

Diagnostics information will be displayed from the Pi via a PiOLED display.

## System Preparation

Instructions to prepare a new headless Raspberry Pi 3 from scratch.

1. [Install Raspbian](https://github.com/tfors/rpi-tf/blob/master/doc/install_raspbian.md)
2. [Build and Install OpenCV](https://github.com/tfors/rpi-tf/blob/master/doc/install_opencv.md)
3. [Build and Install Tensorflow](https://github.com/tfors/rpi-tf/blob/master/doc/install_tensorflow.md)
4. [Install PiOLED, Camera, and Additional Software](https://github.com/tfors/rpi-tf/blob/master/doc/install_pioled.md)
5. [Setup auto-mount of USB thumb drives](https://github.com/tfors/rpi-tf/blob/master/doc/setup_automount.md)
