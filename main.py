from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import ItemEnterEvent, KeywordQueryEvent

import utils


spotify = utils.Spotify()
results = utils.ResultsRenderer()


class ControlSpotifyExtension(Extension):

    def __init__(self):
        super(ControlSpotifyExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())


class ItemEnterEventListener(EventListener):

    def on_event(self, event, _extension):
        spotify.execute_command(event.get_data())
        return results.menu_items(spotify)


class KeywordQueryEventListener(EventListener):

    def on_event(self, _event, extension):
        results.update_preferences(extension.preferences)
        return results.menu_items(spotify)


if __name__ == '__main__':
    ControlSpotifyExtension().run()
