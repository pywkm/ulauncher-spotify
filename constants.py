PLAYER_INTERFACE = 'org.mpris.MediaPlayer2.Player'
PROPERTIES_INTERFACE = 'org.freedesktop.DBus.Properties'
SPOTIFY_PATH = '/usr/share/spotify/spotify.desktop'
BUS_NAME = 'org.mpris.MediaPlayer2.spotify'
PLAYER_PATH = '/org/mpris/MediaPlayer2'


class Actions(object):
    PLAY_PAUSE = 'PlayPause'
    NEXT = 'Next'
    PREVIOUS = 'Previous'


class States(object):
    PAUSED = 'Paused'
    PLAYING = 'Playing'


class Properties(object):
    STATUS = 'PlaybackStatus'
    METADATA = 'Metadata'


class MetadataKeys(object):
    ARTIST = 'xesam:artist'
    TITLE = 'xesam:title'
    ALBUM = 'xesam:album'


class IconPaths(object):
    ICON = 'images/icon.png'
    PLAY = 'images/play.png'
    PAUSE = 'images/pause.png'
    NEXT = 'images/next.png'
    PREVIOUS = 'images/prev.png'
