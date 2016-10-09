Date:     2013-08-15
Subject:  Adventures in Dual Booting
Tags:     debian, linux, dual boot, windows 7, grub
Abstract: Performed a Windows 7 reinstall this weekend.  In the spirit of actually documenting these things so I'm not scrambling off into Google every time I have to do this, this post is a very unscientific description of how I was able to restore GRUB after the install.

## 1. Boot from Debian Install Disc

Do it.

## 2. Start in Recovery Mode

I wasn't able to actually mount the partition until I took this step.

## 3. Switch to a Console (Alt+F2)

Once you activate a console, mount the old Debian partition at `/mnt`:

    # mount /dev/sda5 /mnt

Then, create a symlink to the `boot` directory on that partition at the root of the temporary recovery file system:

    # ln -s /mnt/boot /boot

## 4. From the mounted partition, execute `grub-setup`

I neglected to actually write down where this executable lives (I believe it was somewhere under `lib` in `linux-i386` something or other).  Push comes to shove, just do this:

    # find /mnt -name grub-setup

You should get no error messages.  Then, just reboot and the GRUB menu should reappear.

***Warning:*** *I attempted to run `grub-install` first which complained about not being able to find `/sbin/grub-setup`.  This may have done something before complaining; I'm not sure.*

## Conclusion

Still need to figure out why I'm getting a `error: no such device: {UUID}` when I select windows from the list.  It boots fine but still gives me the warning.
