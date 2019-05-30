---
date:    2019-05-30
subject: Audible Gnome Notifications
tags:
    - gnome
    - linux
    - dbus
    - usability
abstract: |
    A ~150 LOC program for making Gnome's notifications audible by
    monitoring DBus for common notification pathways and playing a
    sound when a message matches a certain pattern.
---

## Usage

Should work out of the box without needing to install any additional
dependencies (tested on CentOS 7 and Fedora 29, 30):

    ./gaudible.py --filter firefox --filter calendar --filter calendar-legacy


## Source ([@dbazile/gaudible](https://github.com/dbazile/gaudible))

```python
#!/usr/bin/python

import argparse
import logging
import os
import subprocess
import sys
import threading
import time

from dbus import SessionBus
from dbus.mainloop.glib import DBusGMainLoop
from glib import MainLoop


DEFAULT_PLAYER = '/usr/bin/paplay'
DEFAULT_FILE   = '/usr/share/sounds/freedesktop/stereo/bell.oga'

FILTERS = {
    'calendar':        ('org.gtk.Notifications', 'AddNotification', 'org.gnome.Evolution-alarm-notify'),
    'calendar-legacy': ('org.freedesktop.Notifications', 'Notify', 'Evolution Reminders'),
    'firefox':         ('org.freedesktop.Notifications', 'Notify', 'Firefox'),
    'test':            ('org.freedesktop.Notifications', 'Notify', 'notify-send'),
}

LOG = logging.getLogger('gaudible')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--debug', action='store_true')
    ap.add_argument('--file', default=DEFAULT_FILE)
    ap.add_argument('--filter', dest='filters', action='append', choices=FILTERS.keys())
    ap.add_argument('--player', default=DEFAULT_PLAYER)
    params = ap.parse_args()

    logging.basicConfig(
        datefmt='%H:%M:%S',
        format='%(asctime)s %(levelname)5s - %(message)s',
        level='DEBUG' if params.debug else 'INFO',
        stream=sys.stdout,
    )

    LOG.debug('Testing for player and audio file')

    if not os.access(params.player, os.R_OK | os.X_OK):
        ap.error('player does not exist or is not executable: %s' % params.player)
    if not os.access(params.file, os.R_OK):
        ap.error('audio file does not exist or is not readable: %s' % params.file)

    LOG.debug('Initializing')

    DBusGMainLoop(set_as_default=True)
    bus = SessionBus()

    filter_keys = tuple(sorted(set(params.filters if params.filters else FILTERS.keys())))

    subscribe_to_messages(bus, filter_keys)

    LOG.debug('Creating audio player')
    audio_player = AudioPlayer(params.player, params.file)

    LOG.debug('Adding message handler')
    attach_message_handler(bus, audio_player, filter_keys)

    LOG.info('ONLINE')

    loop = MainLoop()
    try:
        loop.run()
    except KeyboardInterrupt:
        loop.quit()


def attach_message_handler(bus, audio_player, filter_keys):
    """
    :type bus:          SessionBus
    :type audio_player: AudioPlayer
    :type filter_keys:  tuple

    References:
    - https://developer.gnome.org/notification-spec/
    - https://wiki.gnome.org/Projects/GLib/GNotification
    """

    def on_message(_, msg):
        try:
            interface = msg.get_interface()
            method = msg.get_member()
            args = msg.get_args_list()
            origin = str(args[0])

            for filter_key in filter_keys:
                filter_interface, filter_method, filter_origin = FILTERS[filter_key]

                if filter_interface == interface and filter_method == method and filter_origin == origin:
                    LOG.info('RECEIVE: \033[1m%-15s\033[0m (from=%s:%s, args=%s)', filter_key, interface, method, args)
                    audio_player.play()
                    return

            LOG.debug('DROP: \033[2m%s:%s\033[0m (args=%s)', interface, method, args)

        except Exception as e:
            LOG.error('Something bad happened', exc_info=e)

    bus.add_message_filter(on_message)


def subscribe_to_messages(bus, filter_keys):
    """
    :type bus:         SessionBus
    :type filter_keys: tuple

    References:
    - https://dbus.freedesktop.org/doc/dbus-specification.html#message-bus-routing-match-rules
    """

    rules = []
    for k in filter_keys:
        interface, method, origin = FILTERS[k]
        rule = 'type=method_call, interface=%s, member=%s' % (interface, method)
        LOG.info('Subscribe: \033[1m%-15s\033[0m (rule=%s, origin=%s)', k, repr(rule), repr(origin))
        rules.append(rule)

    proxy = bus.get_object('org.freedesktop.DBus', '/org/freedesktop/DBus')
    proxy.BecomeMonitor(rules, 0, dbus_interface='org.freedesktop.DBus.Monitoring')


class AudioPlayer:
    def __init__(self, player, file_):
        self._player = player
        self._file = file_

    def play(self):
        t = threading.Thread(target=self._play, name='%s:%s' % (self.__class__.__name__, time.time()))
        t.start()

        # HACK: Without this, sometimes the first execution gets deferred until
        #       the process is about to exit.  Probably related to using GLib's
        #       event loop.
        t.join(0.1)

        return t

    def _play(self):
        cmd = [self._player, self._file]
        LOG.debug('EXEC: %s (thread=%s)', cmd, threading.current_thread().name)
        subprocess.check_call(cmd)


if __name__ == '__main__':
    main()
```


## Background

My motivation for writing this is because
[Evolution](https://wiki.gnome.org/Apps/Evolution)'s calendar reminders
don't play sound on a global level.  Unless I stare at my computer all
day (impossible when I'm reading physical documents), it's really easy
to miss the silent appointment reminder popups. The only option
Evolution has to play sound for an appointment is to manually add a
sound for every appointment one by one which I'm sure there's a good
reason for...  Probably. 😶

I _believe_ work is being done in lower-level components of Gnome to
support better customization around notifications but until that lands,
I'm using this to make sure my calendar reminders actually work
properly.


## Known Shortcomings

I kept this program dirt-simple to make it easy to visually inspect for
folks who are as security-paranoid as I am.  There are improvements I'd
make otherwise, specifically:

- Playing a different sound per notification origin (e.g., Firefox,
  Evolution, etc)
- Using Python 3 (would break out-of-the-box compatibility between
  Fedora and CentOS 7)
- Using [GSound](https://wiki.gnome.org/Projects/GSound) instead of
  spawning a new `paplay` process each time
- Throttling "noisy" origins (e.g., instant messaging webapps)


## Other Notes

There is a way to send
["hints"](https://developer.gnome.org/notification-spec/) to the
notifications subsystem that will actually play a sound without the need
for manual wizardry as what I've done, ala:

    notify-send --hint=string:sound-name:alarm-clock-elapsed test

...but the sound name would need to exist in the [freedesktop theme
spec](http://0pointer.de/public/sound-naming-spec.html#notification) and
Evolution would need to send that hint along with its usual notification
message to DBus.

I should submit an Evolution PR for that.  If only I knew C... 🤔
