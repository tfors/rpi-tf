# Install OpenCV on the Raspberry Pi

*September, 2017*

## 1. Install Dependencies

SSH into the raspberry pi and run the following to install the depedencies.

### Developer tools
```
$ sudo apt-get install build-essential git cmake pkg-config
$ sudo apt-get install screen
```

### Image dependencies
```
$ sudo apt-get install libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev
```

### Video dependencies
```
$ sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
$ sudo apt-get install libxvidcore-dev libx264-dev
```

### GUI dependencies
```
$ sudo apt-get install libgtk2.0-dev
```

### Math dependencies
```
$ sudo apt-get install libatlas-base-dev gfortran
```

### Python dependencies
```
$ sudo apt-get install python3-dev python3-pip
$ sudo pip3 install numpy
$ sudo ln -sf /usr/bin/python3 /usr/bin/python
```

## 2. Build OpenCV

### Get source

```
$ wget -O opencv-3.3.0.tgz https://github.com/opencv/opencv/archive/3.3.0.tar.gz
$ tar -xvzf opencv-3.3.0.tgz
$ wget -O opencv_contrib-3.3.0.tgz https://github.com/opencv/opencv_contrib/archive/3.3.0.tar.gz
$ tar -xvzf opencv_contrib-3.3.0.tgz
```

### Prepare for build

```
$ cd ~/opencv-3.0.0/
$ mkdir build
$ cd build
$ cmake -D CMAKE_BUILD_TYPE=RELEASE \
	-D CMAKE_INSTALL_PREFIX=/usr/local \
	-D INSTALL_C_EXAMPLES=ON \
	-D INSTALL_PYTHON_EXAMPLES=ON \
	-D OPENCV_EXTRA_MODULES_PATH=~/src/opencv_contrib-3.3.0/modules \
	-D BUILD_EXAMPLES=ON ..
```

Inspect the output of cmake and verify the Python3 section:

```
--   Python 3:
--     Interpreter:                 /usr/bin/python3 (ver 3.5.3)
--     Libraries:                   /usr/lib/arm-linux-gnueabihf/libpython3.5m.so (ver 3.5.3)
--     numpy:                       /usr/local/lib/python3.5/dist-packages/numpy/core/include (ver 1.13.1)
--     packages path:               lib/python3.5/dist-packages
```

### Build

```
$ screen -S opencv-build
$ make 2>&1 | tee buildLog.out
```

Use Ctrl-A D to disconnect from screen session so you can disconnect and leave the build run.  It will take a long time. You can always check on nthe build progress by connecting again via SSH and:
```
$ tail ~/src/opencv-3.3.0/build/buildLog.out
```

### Install

```
$ sudo make install
$ sudo ldconfig

```
