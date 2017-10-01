# Enable auto-mounting of USB flash drives

*October, 2017*

These instructions have been adapted from those found [here](https://www.raspberrypi.org/forums/viewtopic.php?t=192291)

## 1. Preparing the USB Flash drives

Format a USB flash drive and insert into the Raspberry Pi.  Label it `xfer_a` as shown below.

```
$ sudo e2label /dev/sda1 xfer_a
$ sudo umount /dev/sda1
```
Repeat for a second USB flash drive labeling it `xfer_b`.

## 2. Configure Auto-mounting

Install `pmount`

```
$ sudo apt-get install pmount
```

Create the following file at `/etc/udev/rules.d/usbstick.rules`
```
ACTION=="add", KERNEL=="sd[a-z][0-9]", TAG+="systemd", ENV{SYSTEMD_WANTS}="usbstick-handler@%k"
```

Create the following file at `/lib/systemd/system/usbstick-handler@.service`
```
[Unit]
Description=Mount USB sticks
BindsTo=dev-%i.device
After=dev-%i.device

[Service]
Type=oneshot
RemainAfterExit=yes
ExecStart=/usr/local/bin/automount %I
ExecStop=/usr/bin/pumount /dev/%I
```

Create the following file at ` /usr/local/bin/automount`
```bash
#!/bin/bash

PART=$1
FS_LABEL=`lsblk -o name,label | grep ${PART} | awk '{print $2}'`

if [ -z ${FS_LABEL} ]
then
    /usr/bin/pmount --umask 000 --noatime -w --sync /dev/${PART} /media/${PART}
else
    /usr/bin/pmount --umask 000 --noatime -w --sync /dev/${PART} /media/${FS_LABEL}
fi
```

## 3. Test

Insert the flash drive labeled `xfer_a`, wait for it to automount and confirm that it did indeed mount:
```
$ df | grep media
/dev/sda1       14985608   37504  14163824   1% /media/xfer_a
$ sudo umount /dev/sda1
```
Repeat for the second flash drive.
