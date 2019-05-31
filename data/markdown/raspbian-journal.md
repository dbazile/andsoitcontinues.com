---
date:    2019-02-09
subject: Raspbian Notes
tags:
    - raspberry pi
    - linux
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
