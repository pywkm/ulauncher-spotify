from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.LaunchAppAction import LaunchAppAction
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem

import utils


spotify = utils.Spotify()


class SpotifyEventListener(EventListener):

    def on_event(self, event, extension):
        if not spotify.connected:
            spotify.connect()
        spotify.update_preferences(extension.preferences)


class ControlSpotifyExtension(Extension):

    def __init__(self):
        super(ControlSpotifyExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())


class ItemEnterEventListener(SpotifyEventListener):

    def on_event(self, event, extension):
        super(ItemEnterEventListener, self).on_event(event, extension)
        spotify.execute_command(event.get_data())
        return RenderResultListAction(spotify.menu_items)


class KeywordQueryEventListener(SpotifyEventListener):

    def on_event(self, event, extension):
        super(KeywordQueryEventListener, self).on_event(event, extension)
        if not spotify.connected:
            return RenderResultListAction(
                [
                    ExtensionResultItem(
                        icon='images/icon.png',
                        name='Run Spotify desktop app first',
                        on_enter=LaunchAppAction(spotify.APP_PATH)
                    ),
                ]
            )
        return RenderResultListAction(spotify.menu_items)


if __name__ == '__main__':
    ControlSpotifyExtension().run()
