PLAYER_INTERFACE = 'org.mpris.MediaPlayer2.Player'
PROPERTIES_INTERFACE = 'org.freedesktop.DBus.Properties'
SPOTIFY_PATH = '/usr/share/spotify/spotify.desktop'
BUS_NAME = 'org.mpris.MediaPlayer2.spotify'
PLAYER_PATH = '/org/mpris/MediaPlayer2'


class Actions:
    PLAY_PAUSE = 'PlayPause'
    NEXT = 'Next'
    PREVIOUS = 'Previous'


class States:
    PAUSED = 'Paused'
    PLAYING = 'Playing'


class Properties:
    STATUS = 'PlaybackStatus'
    METADATA = 'Metadata'


class MetadataKeys:
    ARTIST = 'xesam:artist'
    TITLE = 'xesam:title'
    ALBUM = 'xesam:album'


class IconPaths:
    ICON = 'images/icon.png'
    PLAY = 'images/play.png'
    PAUSE = 'images/pause.png'
    NEXT = 'images/next.png'
    PREVIOUS = 'images/prev.png'
