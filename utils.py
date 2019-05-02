import time
import dbus

from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem

import constants as cs


class Spotify(object):

    connected = False
    _preferences = None
    _bus = None
    _interface = None
    _interval = 0.02
    _max_wait = 0.5

    @property
    def status(self):
        return {
            'state': str(self._properties.Get(cs.PLAYER_INTERFACE, cs.Properties.STATUS)),
            'artist': ', '.join(self._metadata[cs.MetadataKeys.ARTIST]).encode('utf8'),
            'title': self._metadata[cs.MetadataKeys.TITLE].encode('utf8'),
            'album': self._metadata[cs.MetadataKeys.ALBUM].encode('utf8'),
        }

    @property
    def keep_open(self):
        return str(self._preferences.get('keep_open')).lower() == 'true'

    @property
    def menu_items(self):
        return [
            ExtensionResultItem(
                icon=cs.IconPaths.PLAY if self.status['state'] == cs.States.PAUSED else cs.IconPaths.PAUSE,
                name='{} - {}'.format(self.status['artist'], self.status['title']),
                description='Album: {}     ({})'.format(self.status['album'], self.status['state']),
                on_enter=ExtensionCustomAction(cs.Actions.PLAY_PAUSE, keep_app_open=self.keep_open),
            ),
            ExtensionResultItem(
                icon=cs.IconPaths.NEXT,
                name='Next track',
                on_enter=ExtensionCustomAction(cs.Actions.NEXT, keep_app_open=self.keep_open),
            ),
            ExtensionResultItem(
                icon=cs.IconPaths.PREVIOUS,
                name='Previous track',
                on_enter=ExtensionCustomAction(cs.Actions.PREVIOUS, keep_app_open=self.keep_open),
            ),
        ]

    def execute_command(self, command):
        old_status = self.status
        getattr(self._interface, command)()
        waited = 0
        # Status might not change if action is 'Previous' and same track is played again
        while self.status == old_status and waited <= self._max_wait:
            time.sleep(self._interval)
            waited += self._interval

    def update_preferences(self, preferences):
        self._preferences = preferences

    def connect(self):
        try:
            self._bus = dbus.SessionBus().get_object(cs.BUS_NAME, cs.PLAYER_PATH)
        except dbus.exceptions.DBusException:
            return
        self.connected = True
        self._interface = dbus.Interface(self._bus, dbus_interface=cs.PLAYER_INTERFACE)

    @property
    def _properties(self):
        return dbus.Interface(self._bus, cs.PROPERTIES_INTERFACE)

    @property
    def _metadata(self):
        return self._properties.Get(cs.PLAYER_INTERFACE, cs.Properties.METADATA)
