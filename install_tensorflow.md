# Preparation

*September, 2017*

## Bazel Dependencies

```
$ sudo apt-get install pkg-config zip g++ zlib1g-dev unzip
$ sudo apt-get install oracle-java7-jdk
$ sudo update-alternatives --config java
```

## Tensorflow Dependencies
```
$ sudo apt-get install python3-pip python3-numpy swig python3-dev
$ sudo pip3 install wheel
```

## Configure for optimization flags
```
$ sudo apt-get install gcc-4.8 g++-4.8
$ sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-4.8 100
$ sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-4.8 100
```

## Prepare to build

```
$ mkdir tensorflow
$ cd tensorflow
```

## Create extra swap space

Insert a thumb drive into a USB port to use as swap space.
```
$ sudo blkid
/dev/sda1: UUID="38E2-7FCB" TYPE="vfat"
$ sudo umount /dev/sda1
$ sudo mkswap /dev/sda1
mkswap: /dev/sda1: warning: wiping old vfat signature.
Setting up swapspace version 1, size = 28.7 GiB (30752616448 bytes)
no label, UUID=139bccd9-a5d6-b45c-3ae3-deca7c690ee7
```

Edit `/etc/fstab` and add the line:
```
UUID=139bccd9-a5d6-b45c-3ae3-deca7c690ee7 none swap sw,pri=5 0 0
```

Run the following to enable swap:
```
$ sudo swapon -a
```

# Build Bazel
```
$ wget https://github.com/bazelbuild/bazel/releases/download/0.5.4/bazel-0.5.4-dist.zip
$ unzip -d bazel bazel-0.5.4-dist.zip
$ cd bazel
```

Edit `scripts/bootstrap/compile.sh` and change line 122:
```
run "${JAVAC}" -classpath "${classpath}" -sourcepath "${sourcepath}" \
       -d "${output}/classes" -source "$JAVA_VERSION" -target "$JAVA_VERSION" \
       -encoding UTF-8 "@${paramfile}"
```
Add `-J-Xmx500M` at end of command:
```
run "${JAVAC}" -classpath "${classpath}" -sourcepath "${sourcepath}" \
       -d "${output}/classes" -source "$JAVA_VERSION" -target "$JAVA_VERSION" \
       -encoding UTF-8 "@${paramfile}" -J-Xmx500M
```

Build bazel (this will take some time, so run in a screen session so you can disconnect.):
```
$ screen -S bazel-build
$ sudo ./compile.sh 2>&1 | tee buildLog.out
```
When the build is done, install bazel:
```
$ sudo cp output/bazel /usr/local/bin/bazel
```

# Build Tensorflow
```
$ git clone --recurse-submodules https://github.com/tensorflow/tensorflow.git
$ cd tensorflow
$ git checkout v1.3.0
```

Change all references to 64-bit binaries to 32-bit:
```
$ grep -Rl 'lib64' | xargs sed -i 's/lib64/lib/g'
```
Edit `tensorflow/core/platform/platform.h` and delete the line defining the arm architecture as a mobile platform (line 48):
```
#elif defined(__arm__)
#define PLATFORM_POSIX
...
#define IS_MOBILE_PLATFORM   <----- DELETE THIS LINE
```
Update the version of eigen with fixes for Raspberry Pi ARM/Neon. Edit `tensorflow/workspace.bzl` and change:
```
native.new_http_archive(
    name = "eigen_archive",
    urls = [
        "http://mirror.bazel.build/bitbucket.org/eigen/eigen/get/f3a22f35b044.tar.gz",
        "https://bitbucket.org/eigen/eigen/get/f3a22f35b044.tar.gz",
    ],
    sha256 = "ca7beac153d4059c02c8fc59816c82d54ea47fe58365e8aded4082ded0b820c4",
    strip_prefix = "eigen-eigen-f3a22f35b044",
    build_file = str(Label("//third_party:eigen.BUILD")),
)
```
To:
```
native.new_http_archive(
    name = "eigen_archive",
    urls = [
        "http://mirror.bazel.build/bitbucket.org/eigen/eigen/get/d781c1de9834.tar.gz",
        "https://bitbucket.org/eigen/eigen/get/d781c1de9834.tar.gz",
    ],
    sha256 = "a34b208da6ec18fa8da963369e166e4a368612c14d956dd2f9d7072904675d9b",
    strip_prefix = "eigen-eigen-d781c1de9834",
    build_file = str(Label("//third_party:eigen.BUILD")),
)
```

Configure the build and accept the defaults:
```
$ ./configure
```

Start the build:
```
$ screen -S tf-build
$ bazel build -c opt --copt="-mfpu=neon-vfpv4" \
    --copt="-funsafe-math-optimizations" \
    --copt="-ftree-vectorize" \
    --copt="-fomit-frame-pointer" \
    --local_resources 1024,1.0,1.0 \
    --verbose_failures tensorflow/tools/pip_package:build_pip_package \
    2>&1 | tee buildLog.out

```

Build the pip package and install it:
```
$ bazel-bin/tensorflow/tools/pip_package/build_pip_package /tmp/tensorflow_pkg
$ sudo pip3 install /tmp/tensorflow_pkg/tensorflow-1.3.0-cp35-cp35m-linux_armv7l.whl
```

# Cleanup

Remove the swap partition
```
$ lsblk
NAME        MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
sda           8:0    1 28.7G  0 disk
└─sda1        8:1    1 28.7G  0 part [SWAP]
mmcblk0     179:0    0 28.8G  0 disk
├─mmcblk0p1 179:1    0 41.8M  0 part /boot
└─mmcblk0p2 179:2    0 28.8G  0 part /

$ sudo swapoff /dev/sda1
```

Edit `/etc/fstab` and remove the following line:
```
UUID=139bccd9-a5d6-b45c-3ae3-deca7c690ee7 none swap sw,pri=5 0 0
```
Reboot the Raspberry Pi.
