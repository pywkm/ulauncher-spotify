import time
import dbus

from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem


def boolify(string):
    return string.lower() == 'true'


class Spotify(object):

    PLAYER_INTERFACE = 'org.mpris.MediaPlayer2.Player'
    PROPERTIES_INTERFACE = 'org.freedesktop.DBus.Properties'
    APP_PATH = '/usr/share/spotify/spotify.desktop'
    BUS_NAME = 'org.mpris.MediaPlayer2.spotify'
    PLAYER_PATH = '/org/mpris/MediaPlayer2'

    connected = False
    _preferences = None
    _bus = None
    _interface = None

    @property
    def status(self):
        return {
            'state': str(self._properties.Get(self.PLAYER_INTERFACE, 'PlaybackStatus')),
            'artist': ', '.join(self._metadata['xesam:artist']).encode('utf8'),
            'track': self._metadata['xesam:title'].encode('utf8'),
            'album': self._metadata['xesam:album'].encode('utf8'),
        }

    @property
    def keep_open(self):
        return boolify(self._preferences.get('keep_open'))

    @property
    def menu_items(self):
        return [
            ExtensionResultItem(
                icon='images/play.png' if self.status['state'] == 'Paused' else 'images/pause.png',
                name='{} - {}'.format(self.status['artist'], self.status['track']),
                description='Album: {}     ({})'.format(self.status['album'], self.status['state']),
                on_enter=ExtensionCustomAction('PlayPause', keep_app_open=self.keep_open),
            ),
            ExtensionResultItem(
                icon='images/next.png',
                name='Next track',
                on_enter=ExtensionCustomAction('Next', keep_app_open=self.keep_open),
            ),
            ExtensionResultItem(
                icon='images/prev.png',
                name='Previous track',
                on_enter=ExtensionCustomAction('Previous', keep_app_open=self.keep_open),
            ),
        ]

    def execute_command(self, command):
        old_status = self.status
        getattr(self._interface, command)()
        while self.status == old_status:
            time.sleep(0.02)

    def update_preferences(self, preferences):
        self._preferences = preferences

    def connect(self):
        try:
            self._bus = dbus.SessionBus().get_object(self.BUS_NAME, self.PLAYER_PATH)
        except dbus.exceptions.DBusException:
            return
        self.connected = True
        self._interface = dbus.Interface(self._bus, dbus_interface=self.PLAYER_INTERFACE)

    @property
    def _properties(self):
        return dbus.Interface(self._bus, self.PROPERTIES_INTERFACE)

    @property
    def _metadata(self):
        return self._properties.Get(self.PLAYER_INTERFACE, 'Metadata')
