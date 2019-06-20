import dbus
import collections
import time

from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.action.LaunchAppAction import LaunchAppAction
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem

import constants as cs


Status = collections.namedtuple('Status', 'playback_status artist title album')


class Spotify:

    connected = False
    _interval = 0.02
    _max_wait = 1

    @property
    def status(self):
        return Status(
            playback_status=self._properties.Get(cs.PLAYER_INTERFACE, cs.Properties.STATUS),
            artist=', '.join(self._metadata[cs.MetadataKeys.ARTIST]),
            title=self._metadata[cs.MetadataKeys.TITLE],
            album=self._metadata[cs.MetadataKeys.ALBUM],
        )

    def execute_command(self, command):
        old_status = self.status
        getattr(self._interface, command)()
        waited = 0
        # Status might not change if action is 'Previous' and same track is played again
        while self.status == old_status and waited <= self._max_wait:
            time.sleep(self._interval)
            waited += self._interval

    @property
    def _bus(self):
        return dbus.SessionBus().get_object(cs.BUS_NAME, cs.PLAYER_PATH)

    @property
    def _interface(self):
        return dbus.Interface(self._bus, dbus_interface=cs.PLAYER_INTERFACE)

    @property
    def _properties(self):
        return dbus.Interface(self._bus, cs.PROPERTIES_INTERFACE)

    @property
    def _metadata(self):
        return self._properties.Get(cs.PLAYER_INTERFACE, cs.Properties.METADATA)


class ResultsRenderer:
    _preferences = None
    _name_line = None
    _description_line = None

    def update_preferences(self, preferences):
        self._preferences = preferences
        self._set_formatting()

    @property
    def keep_open(self):
        return str(self._preferences.get('keep_open')).lower() == 'true'

    def menu_items(self, spotify):
        try:
            return self._control_panel(spotify.status)
        except dbus.exceptions.DBusException:
            return self._spotify_not_launched()

    @staticmethod
    def _spotify_not_launched():
        return RenderResultListAction([
            ExtensionResultItem(
                icon=cs.IconPaths.ICON,
                name='Run Spotify desktop app first',
                on_enter=LaunchAppAction(cs.SPOTIFY_PATH)
            ),
        ])

    def _control_panel(self, spotify_status):
        return RenderResultListAction([
            ExtensionResultItem(
                icon=cs.IconPaths.PLAY if spotify_status.playback_status == cs.States.PAUSED else cs.IconPaths.PAUSE,
                name=self._format(self._name_line, spotify_status),
                description=self._format(self._description_line, spotify_status),
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
        ])

    def _set_formatting(self):
        formatting = self._preferences.get('custom_format')
        try:
            name_line, description_line = formatting.split('\n', 1)
            description_line = description_line.split('\n')[0]
        except ValueError:
            name_line = formatting
            description_line = ''
        self._name_line, self._description_line = name_line, description_line

    @staticmethod
    def _format(template, spotify_status):
        try:
            return template.format(**spotify_status._asdict())
        except ValueError as err:
            return '{}: "{}"'.format(err, template)
        except KeyError as err:
            return 'Unknown tag "{}" in: "{}"'.format(err, template)
        except IndexError:
            return 'Too many {{}}: "{}"'.format(template)
