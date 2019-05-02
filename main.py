import time
import dbus
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.LaunchAppAction import LaunchAppAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem


player_interface = 'org.mpris.MediaPlayer2.Player'
properties_interface = 'org.freedesktop.DBus.Properties'
spotify_app_path = '/usr/share/spotify/spotify.desktop'
spotify_bus_name = 'org.mpris.MediaPlayer2.spotify'
player_object_path = '/org/mpris/MediaPlayer2'


def boolify(string):
    return string.lower() == 'true'


def get_spotify_bus():
    return dbus.SessionBus().get_object(spotify_bus_name, player_object_path)


def get_menu_items(spotify_bus, keep_open=True):
    spotify_properties = dbus.Interface(spotify_bus, properties_interface)
    meta_data = spotify_properties.Get(player_interface, 'Metadata')
    status = spotify_properties.Get(player_interface, 'PlaybackStatus')
    artist_name = ', '.join(meta_data['xesam:artist']).encode('utf8')
    track_name = meta_data['xesam:title'].encode('utf8')
    album_name = meta_data['xesam:album'].encode('utf8')
    items = [
        ExtensionResultItem(
            icon='images/play.png' if status == 'Paused' else 'images/pause.png',
            name='{} - {}'.format(artist_name, track_name),
            description='Album: {}     ({})'.format(album_name, status),
            on_enter=ExtensionCustomAction('PlayPause', keep_app_open=keep_open),
        ),
        ExtensionResultItem(
            icon='images/next.png',
            name='Next track',
            on_enter=ExtensionCustomAction('Next', keep_app_open=keep_open),
        ),
        ExtensionResultItem(
            icon='images/prev.png',
            name='Previous track',
            on_enter=ExtensionCustomAction('Previous', keep_app_open=keep_open),
        ),
    ]
    return items


class ControlSpotifyExtension(Extension):

    def __init__(self):
        super(ControlSpotifyExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())


class ItemEnterEventListener(EventListener):

    def on_event(self, event, extension):
        command = event.get_data()
        spotify_bus = get_spotify_bus()
        interface = dbus.Interface(spotify_bus, dbus_interface=player_interface)
        getattr(interface, command)()

        # nasty hack so song title has time to update
        time.sleep(0.1)
        return RenderResultListAction(get_menu_items(spotify_bus))


class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        try:
            spotify_bus = get_spotify_bus()
        except dbus.exceptions.DBusException:
            return RenderResultListAction(
                [
                    ExtensionResultItem(
                        icon='images/icon.png',
                        name='Run Spotify desktop app first',
                        on_enter=LaunchAppAction(spotify_app_path)
                    ),
                ]
            )
        keep_open = boolify(extension.preferences.get('keep_open'))
        return RenderResultListAction(get_menu_items(spotify_bus, keep_open))


if __name__ == '__main__':
    ControlSpotifyExtension().run()
