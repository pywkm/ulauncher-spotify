from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent

import utils


spotify = utils.Spotify()
results = utils.ResultsRenderer()


class SpotifyEventListener(EventListener):

    def on_event(self, event, extension):
        if not spotify.connected:
            spotify.connect()
        results.update_preferences(extension.preferences)


class ControlSpotifyExtension(Extension):

    def __init__(self):
        super(ControlSpotifyExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())


class ItemEnterEventListener(SpotifyEventListener):

    def on_event(self, event, extension):
        super(ItemEnterEventListener, self).on_event(event, extension)
        spotify.execute_command(event.get_data())
        return results.menu_items(spotify.status)


class KeywordQueryEventListener(SpotifyEventListener):

    def on_event(self, event, extension):
        super(KeywordQueryEventListener, self).on_event(event, extension)
        if not spotify.connected:
            return results.no_spotify_launched()
        return results.menu_items(spotify.status)


if __name__ == '__main__':
    ControlSpotifyExtension().run()
