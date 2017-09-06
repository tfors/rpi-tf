# Install

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

## Build Bazel
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

## Build Tensorflow
```
$ git clone --recurse-submodules https://github.com/tensorflow/tensorflow.git
$ cd tensorflow
$ git checkout v1.3.0
```
