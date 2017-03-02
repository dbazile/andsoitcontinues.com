---
date:    2013-09-10
subject: Wifi Overcrowding
tags:
    - wifi
    - troubleshooting
    - router
abstract: |
    Labor Day weekend was plagued by intermittent WiFi issues.
    Streaming was effectively impossible as ping times were sky high
    and Netflix buffering was occurring once every two minutes.  The
    following is the historical log of events.  Names have been
    changed to protect the innocent.
---

Naturally, the first instinct was to assume it's all Comcast's fault.  After multiple speed tests and finally calling Comcast on Sunday to see if there was an issue on their end, I managed to narrow it down to network traffic on the router.  Ping times from my laptop to my modem's IP yielded a 3-digit ping time -- *Yikes*.  So now that I know that the issue lives on my LAN, I set out to fix the issue.

## Why does my router hate me?

I `ping -f` the router to see that this thing is dropping packets like crazy.  The router is running *802.11b/g/n* on dual bands.  I try changing channels, setting wireless interference mitigation mode and a whole bunch of other things.  No lasting impact.  While wired connections to the router would yield a ping time around 1ms, pinging the router from any wireless node ranged between 200 and 600ms.

## Maybe it's interference?

There are upwards of 30 SSID's broadcasting in detectable range of our apartment, many of them clustered on the same channels.  There are a vast assortment of protocols from *802.11a* thru *n*.  For a moment during one incident, I noticed that while the MacBook and iPhones were experiencing terrible latency, the Inspiron was chugging along without much issue at a much lower ping time.  The Inspiron was on *wireless-g* and the MacBook and iPhones *wireless-n*.  I tried moving those devices from *n* to *g* and the issue seemed to go away for a while.  Ping times were consistently around 15-40ms.

## Later that night...

Problem manifests itself again later that night when we're trying to watch Netflix (seriously, WiFi?  Now?).  Ping is through the roof on all wireless nodes *and they're all on wireless-g*.  At this point, I start having a suspicion that the router is going bad and am considering just running to Best Buy to pick up a new one.  It just so happened that they would have been closed for the night by the time I got there, so I continue fumbling around in the dark trying to fix this with every possible unscientific method.

I switched off WMM on the 2.4GHz adapter, bumped its transmit power to 200 and still no joy.  I bring up the device status page to see the signal quality for all connected devices.  I noticed that the MacBook -- not being used but set to automatically wake at 8PM and sleep at midnight -- was still connected to the router.  I ssh in and run a quick `shutdown -h now` to kick it off the net.  Mysteriously, ping drops to <50ms.  W...T...F...?

## Conclusion

Still no clue as to what is actually at issue here.  It's very possible that my router is failing and I am witnessing its death throes.  It's also possible that there are enough wireless signals in this building to interfere with NASA.  So the ultimate experiment control comes when we move out of this place.

###### Update 2013-09-12

The issue *seems* to have ceased since then.  I still have no clue as to what was actually causing the issue.  I am inclined to believe that it was the MacBook's fault -- it is getting rather old and maybe the wifi card is failing (is this even a thing)?  All I know is that since disabling the MacBook's scheduled wake-up, the issue has not resurfaced.  Do I think my MacBook is DDoS'ing my LAN?  Is this issue even resolved?  Time will tell.


### Further Reading:

1.  [Coping with Wi-Fi's biggest problem: interference](http://www.networkworld.com/news/tech/2010/080210-wifi-interference.html)

