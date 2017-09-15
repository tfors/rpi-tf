# Install PiOLED, Camera, and Additional Software

*September, 2017*

## 1. PiOLED

### Installing the PiOLED

The [PiOLED](https://www.adafruit.com/product/3527) display is simple to install.  It arrives fully assembled and plugs directly into the i2c pins of the I/O header on the Raspberry Pi 3.

### Installing Supporting Software
```
$ sudo pip3 install RPi.GPIO
$ sudo apt-get install python3-smbus
$ cd src
$ git clone https://github.com/adafruit/Adafruit_Python_SSD1306.git
$ cd Adafruit_Python_SSD1306
$ sudo python setup.py install
$ sudo apt-get install -y i2c-tools
```

### Enable i2c
```
$ sudo raspi-config
```

Choose Interface and enable i2c.  Exit the config software and reboot.
```
$ sudo shutdown -r now
```

## 2. Camera

### Install Supporting Software

```
$ sudo pip3 install imutils picamera
```

### Enable Camera
```
$ sudo raspi-config
```

Choose Interface and enable camera.  Exit the config software and reboot.
```
$ sudo shutdown -r now
```
