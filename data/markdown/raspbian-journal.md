---
date:    2019-10-12
subject: Raspbian Notes (Updated)
tags:
    - raspberry pi
    - linux
    - keyboard
    - udev
abstract: |
    Keeping a few notes in an easy-to-reach place lest I forget (or
    end up having to reimage the disk after wrecking things beyond
    repair and forgetting to back stuff up first...)
---

## Setup

- Raspberry Pi 3 B+
- Raspbian Stretch Lite
- Logitech K375s (wireless via USB Unifying Receiver)
- Monitor (via HDMI)


## Fixing Keyboard Annoyances

![keyboard and receiver](/public/writing/attachments/k375s.png)

My Logitech K375s via the unifying receiver works properly except but
some of the keys were all a-poopy, i.e.:

- **Home** and **End** cycle between ttys (just weird)
- **Right-Control** key would behave like a special character insert
key (may be standard on non-US keyboards, I dunno)

No luck trying to change the locale/layout with `raspi-config`, but
appending this to `/etc/console-setup/cached_keyboard_setup.sh`
worked:

```bash
kbdrate -d 175 -r 200
loadkeys <<-EOT
	keymaps 0-255

	# make capslock another escape key
	keycode 50 = Escape

	# fix right control key
	keycode 100 = Control

	# fix home key
	keycode 105 = Left
	alt keycode 105 = Home

	# fix end key
	keycode 106 = Right
	alt keycode 106 = End
EOT
```


## Pinning hardware device identifiers

![TP-Link TL-WN7222N](/public/writing/attachments/tplink-TL-WN722N.jpg)

I'm using the above-pictured [TP-Link TL-WN7222N v3](
https://www.tp-link.com/us/home-networking/usb-adapter/tl-wn722n/) USB
Wi-Fi adapter which is capable of entering "monitor" mode.  To
actually _put_ it into monitor mode though, you need [a specialized `rtl8188eu` driver](
https://github.com/aircrack-ng/rtl8188eus).  After compiling,
I manually tested and confirmed that it was working:

    $ sudo insmod /lib/modules/4.19.66-v7++/kernel/drivers/net/wireless/8188eu.ko
    $ sudo iwconfig wlan1 mode monitor

...and then I rebooted. :)

When the machine came back up, I reran the same `iwconfig` command
which gave this error:

    Error for wireless request "Set Mode" (8B06) :
        SET failed on device wlan1 ; Operation not supported.

Apparently the reboot reordered my WLAN devices (maybe because
`8188eu` occurs before both the on-board Wi-Fi's `brcmfmac` driver and
the default `r8188eu` driver in lexical order?).

I ended up adding this [udev rule](https://linux.die.net/man/7/udev)
to pin the device ID to something predictable:

```bash
sudo tee /etc/udev/rules.d/tplink_wlan.rules <<< \
    'SUBSYSTEM=="net", ATTRS{idVendor}=="2357", ATTRS{idProduct}=="010c", NAME="tplink"'
```

To get the values to specify in `ATTRS{...}`, I used `lsusb`:

    $ sudo lsusb
    Bus 001 Device 004: ID 046d:c52b Logitech, Inc. Unifying Receiver
    Bus 001 Device 009: ID 2357:010c TP-Link TL-WN722N v2
    Bus 001 Device 006: ID 0424:7800 Standard Microsystems Corp.
    Bus 001 Device 003: ID 0424:2514 Standard Microsystems Corp. USB 2.0 Hub
    Bus 001 Device 002: ID 0424:2514 Standard Microsystems Corp. USB 2.0 Hub
    Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub

    $ lsusb -d 2357:010c
    Bus 001 Device 009: ID 2357:010c TP-Link TL-WN722N v2

    $ lsusb -d 2357:010c -v
    Bus 001 Device 009: ID 2357:010c TP-Link TL-WN722N v2
    Device Descriptor:
      bLength                18
      bDescriptorType         1
      bcdUSB               2.00
      bDeviceClass            0 (Defined at Interface level)
      bDeviceSubClass         0
      bDeviceProtocol         0
      bMaxPacketSize0        64
      idVendor           0x2357 TP-Link          <------- this is what we're looking for
      idProduct          0x010c TL-WN722N v2     <------- this too...
      bcdDevice            0.00
      iManufacturer           1 Realtek
      iProduct                2 802.11n NIC
      iSerial                 3 00E04C0001
      bNumConfigurations      1
      Configuration Descriptor:
        bLength                 9
        bDescriptorType         2
        wTotalLength           39
        bNumInterfaces          1
        bConfigurationValue     1
        iConfiguration          0
        bmAttributes         0xa0
          (Bus Powered)
          Remote Wakeup
        MaxPower              500mA
        Interface Descriptor:
          bLength                 9
          bDescriptorType         4
          bInterfaceNumber        0
          bAlternateSetting       0
          bNumEndpoints           3
          bInterfaceClass       255 Vendor Specific Class
          bInterfaceSubClass    255 Vendor Specific Subclass
          bInterfaceProtocol    255 Vendor Specific Protocol
          iInterface              0
          Endpoint Descriptor:
            bLength                 7
            bDescriptorType         5
            bEndpointAddress     0x81  EP 1 IN
            bmAttributes            2
              Transfer Type            Bulk
              Synch Type               None
              Usage Type               Data
            wMaxPacketSize     0x0200  1x 512 bytes
            bInterval               0
          Endpoint Descriptor:
            bLength                 7
            bDescriptorType         5
            bEndpointAddress     0x02  EP 2 OUT
            bmAttributes            2
              Transfer Type            Bulk
              Synch Type               None
              Usage Type               Data
            wMaxPacketSize     0x0200  1x 512 bytes
            bInterval               0
          Endpoint Descriptor:
            bLength                 7
            bDescriptorType         5
            bEndpointAddress     0x03  EP 3 OUT
            bmAttributes            2
              Transfer Type            Bulk
              Synch Type               None
              Usage Type               Data
            wMaxPacketSize     0x0200  1x 512 bytes
            bInterval               0
    Device Qualifier (for other device speed):
      bLength                10
      bDescriptorType         6
      bcdUSB               2.00
      bDeviceClass            0 (Defined at Interface level)
      bDeviceSubClass         0
      bDeviceProtocol         0
      bMaxPacketSize0        64
      bNumConfigurations      1
    Device Status:     0x0002
      (Bus Powered)
      Remote Wakeup Enabled

The [Arch Wiki](
https://wiki.archlinux.org/index.php/Udev#Setting_static_device_names)
pointed me in the general direction sort of, but finding this
attribute information was... not intuitive.  Sometimes I think
hardware people don't like documentation. 🤕
