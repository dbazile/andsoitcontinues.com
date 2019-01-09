---
date:    2019-01-08
subject: Watching Hulu and Prime Video in Firefox on Fedora
tags:
    - linux
    - fedora
    - firefox
    - drm
    - widevine
abstract: |
    I accidentally discovered how to get Firefox on Fedora to play Hulu
    and Amazon Prime Videos and I'm finally Chrome-free again. &#127881;.
---

## TL;DR

The following worked on my Fedora 28/29 daily driver:

```
    sudo dnf install \
        https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-28.noarch.rpm \
        https://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-28.noarch.rpm

    sudo dnf install \
        compat-ffmpeg28 \
        ffmpeg-libs \
        ffmpeg \
        gstreamer \
        gstreamer-ffmpeg \
        gstreamer-plugins-bad \
        gstreamer-plugins-bad-free \
        gstreamer-plugins-bad-nonfree \
        gstreamer-plugins-base \
        gstreamer-plugins-good \
        gstreamer-plugins-ugly \
        gstreamer-plugin-crystalhd \
        gstreamer1-plugins-bad-freeworld \
        gstreamer1-plugins-bad-free \
        gstreamer1-plugins-good \
        gstreamer1-libav

    # maybe
    sudo dnf install openh264 mozilla-openh264

    # maybe maybe (read below for more details on if you need this)
    restorecon -R -v ~/.mozilla
```


## Background

Since moving from Ubuntu to Fedora, I couldn't use Firefox to do any
streaming other than YouTube.  Even Twitter's "GIFs" autoconversion
would show a static preview but gave me a "your browser can't play
this video" when clicked.

So I installed the `gstreamer-*` packages via RPM Fusion which
worked for the Twitter "GIFs" but not Amazon or Hulu:

![screenshot of the crash](/writing/attachments/widevine_plugin_crashed.png)

To deal with this, I started running Chrome (which I use only for
Flash holdouts; looking at you Rosetta Stone) to stream and Firefox
for everything else.

### Several months later...

While experimenting with systemd service units this week, I ran into
an SELinux problem.  In researching the fix and more general info on
SELinux, I stumble upon the solution to my Widevine crashing problem
in [this talk from Red Hat Summit 2012](https://www.youtube.com/watch?v=MxjenQ31b70).

Halfway through this video, I decided to take another shot at the
streaming problem and watch `/var/log/messages` for weird SELinux
warnings.

Sure enough, there it was (I added linebreaks for readability):

    Jan  8 20:24:11 kefka python3[2408]: SELinux is preventing plugin-containe from execute access on the file /home/david/.mozilla/firefox/xxxxxxxx.default/gmp-widevinecdm/4.10.1196.0/libwidevinecdm.so.

    *****  Plugin restorecon (57.3 confidence) suggests   ************************

    If you want to fix the label.
    /home/david/.mozilla/firefox/xxxxxxxx.default/gmp-widevinecdm/4.10.1196.0/libwidevinecdm.so default label should be mozilla_home_t.
    Then you can run restorecon. The access attempt may have been stopped due to insufficient permissions to access a parent directory in which case try to change the following command accordingly.
    Do
    # /sbin/restorecon -v /home/david/.mozilla/firefox/xxxxxxxx.default/gmp-widevinecdm/4.10.1196.0/libwidevinecdm.so

    *****  Plugin mozplugger (43.1 confidence) suggests   ************************

    If you want to use the plugin package
    Then you must turn off SELinux controls on the Firefox plugins.
    Do
    # setsebool -P unconfined_mozilla_plugin_transition 0

    *****  Plugin catchall (1.06 confidence) suggests   **************************

    If you believe that plugin-containe should be allowed execute access on the libwidevinecdm.so file by default.
    Then you should report this as a bug.
    You can generate a local policy module to allow this access.
    Do
    allow this access for now by executing:
    # ausearch -c 'plugin-containe' --raw | audit2allow -M my-plugincontaine
    # semodule -X 300 -i my-plugincontaine.pp

Oh, the problem this whole time was a misconfigured SELinux context. :|

### How did the context change?

Here's my hunch.  Last year, I handed down my old Thinkpad to my
eldest child after migrating a bunch of stuff from my home directory
via SCP. The `~/.mozilla` tree apparently inherited the context of
`/home/david` (i.e., `user_home_t`) instead of the correct one (i.e.,
`mozilla_home_t`) which I assume would have been set during the normal
user onboarding/postinstall process.

To see the **correct** default context for the `~/.mozilla` tree, run:

    $ grep '\.mozilla' /etc/selinux/targeted/contexts/files/file_contexts.homedirs

    /home/[^/]+/\.mozilla(/.*)?	unconfined_u:object_r:mozilla_home_t:s0

To see what yours is actually set to, run:

    $ find ~/.mozilla -name '*widevine*.so' -exec ls -lZ {} \;

    -rwx------. 1 david david unconfined_u:object_r:mozilla_home_t:s0 6998236 Dec 30 14:38 /home/david/.mozilla/firefox/xxxxxxxx.default/gmp-widevinecdm/4.10.1196.0/libwidevinecdm.so

If it's set to anything other than `mozilla_home_t` (such as
`user_home_t` like mine was), SELinux is going to restrict Firefox
from loading the plugin and you're gonna get the same ambiguous error
I got in the screenshot above.


## See a problem?

Let me know via [GitHub issue](https://github.com/dbazile/bazile.org/issues/new)
or hit me up on the Twitters [@spoonchucks](https://twitter.com/spoonchucks).


## References:

1. [RPM Fusion Configuration Instructions](https://rpmfusion.org/Configuration)
2. [SELinux for Mere Mortal (Red Hat Summit 2012)](https://www.youtube.com/watch?v=MxjenQ31b70)
