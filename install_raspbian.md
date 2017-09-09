# Install the Raspbian Image on a Micro SD Card

*September, 2017*

1. Download the **Raspbian Stretch Lite** image from [here](https://www.raspberrypi.org/downloads/raspbian/).  The version used in these notes is dated 2017-08-16.

2. Verify the sha-256 hash of the downloaded file matches the hash posted on the download web page:
```
$ sha256sum 2017-08-16-raspbian-stretch-lite.zip
52e68130c152895905abe66279dd9feaa68091ba55619f5b900f2ebed381427b  2017-08-16-raspbian-stretch-lite.zip
```

3. Instructions for preparing the microSD card are provided [here](https://www.raspberrypi.org/documentation/installation/installing-images/linux.md) and may differ slightly from the steps below which have been customized for my Ubuntu 16.04 system.

4. Run `lsblk` to see the existing drives in your system:
```
$ lsblk
NAME           MAJ:MIN RM   SIZE RO TYPE  MOUNTPOINT
nvme0n1        259:0    0   477G  0 disk  
├─nvme0n1p1    259:1    0   600M  0 part  /boot/efi
├─nvme0n1p2    259:2    0     3G  0 part  
├─nvme0n1p3    259:3    0 457.6G  0 part  /
└─nvme0n1p4    259:4    0  15.8G  0 part  
  └─cryptswap1 252:0    0  15.8G  0 crypt [SWAP]
```

5. Insert the microSD card and re-run `lsblk`:
```
$ lsblk
NAME           MAJ:MIN RM   SIZE RO TYPE  MOUNTPOINT
mmcblk0        179:0    0  28.8G  0 disk  
└─mmcblk0p1    179:1    0  28.8G  0 part  /media/user/4CD4-DC26
nvme0n1        259:0    0   477G  0 disk  
├─nvme0n1p1    259:1    0   600M  0 part  /boot/efi
├─nvme0n1p2    259:2    0     3G  0 part  
├─nvme0n1p3    259:3    0 457.6G  0 part  /
└─nvme0n1p4    259:4    0  15.8G  0 part  
  └─cryptswap1 252:0    0  15.8G  0 crypt [SWAP]
```

6. The microSD card appears as `/dev/mmcblk0` with a single partition: `/dev/mmcblk0p1`.  Unmount all partitions.
```
$ df -h | grep mmcblk0
/dev/mmcblk0p1         29G   32K   29G   1% /media/user/4CD4-DC26
$ umount /dev/mmcblk0p1
$ df -h | grep mmcblk0
```

7. Write the Raspbian image to the microSD card and run `sync` when done:
```
$ unzip -p 2017-08-16-raspbian-stretch-lite.zip | sudo dd of=/dev/mmcblk0 status=progress
[sudo] password for user:
1842389504 bytes (1.8 GB, 1.7 GiB) copied, 298 s, 6.2 MB/s
3621912+0 records in
3621912+0 records out
1854418944 bytes (1.9 GB, 1.7 GiB) copied, 304.992 s, 6.1 MB/s
$ sync
```

8. Remove and re-insert the microsSD card.  It should show two partitions now:
```
$ lsblk
NAME           MAJ:MIN RM   SIZE RO TYPE  MOUNTPOINT
mmcblk0        179:0    0  28.8G  0 disk  
├─mmcblk0p1    179:1    0  41.8M  0 part  /media/user/boot
└─mmcblk0p2    179:2    0   1.7G  0 part  /media/user/28590797-4810-4851-b4ec-b
nvme0n1        259:0    0   477G  0 disk  
├─nvme0n1p1    259:1    0   600M  0 part  /boot/efi
├─nvme0n1p2    259:2    0     3G  0 part  
├─nvme0n1p3    259:3    0 457.6G  0 part  /
└─nvme0n1p4    259:4    0  15.8G  0 part  
  └─cryptswap1 252:0    0  15.8G  0 crypt [SWAP]
```

9. Enable SSH on the boot partition of the microSD card:
```
$ touch /media/user/boot/ssh
```

10. Configure the pi to auto-connect to your wifi:
```
$ sudo vim /media/user/28590797-4810-4851-b4ec-bf9672c2918c/etc/wpa_supplicant/wpa_supplicant.conf
```
Change the file to the following:
```
country=US
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
network={
  ssid="WIFI-SSID"
  psk="PASSWORD"
}
```

11. Unmount and eject the microSD card and install in the raspberry Pi.  Boot the Pi and scan for it on the wifi network:
```
$ sudo nmap -p22 -sS 192.168.1.0/28
Starting Nmap 7.01 ( https://nmap.org ) at 2017-09-04 13:16 CDT
Nmap scan report for 192.168.1.3
Host is up (0.0056s latency).
PORT   STATE SERVICE
22/tcp open  ssh
MAC Address: B8:27:EB:XX:XX:XX (Raspberry Pi Foundation)
Nmap done: 3 IP addresses (2 hosts up) scanned in 0.32 seconds
```

12. SSH into the pi as user `pi` and password `raspberry`.  Immediately change the password with `passwd` to a strong random password and perhaps add a public key for future login security.

13. Apply software updates:
```
pi@raspberrypi:~ $ sudo apt-get update
pi@raspberrypi:~ $ sudo apt-get upgrade
pi@raspberrypi:~ $ sudo reboot
```
```
pi@raspberrypi:~ $ sudo rpi-update
pi@raspberrypi:~ $ sudo reboot
```
