# ulauncher-spotify
### Screenshots:
[Ulauncher](https://ulauncher.io/) extension for controlling Spotify

![screenshot](images/screenshot.png)

### Current track formatting:
Formatting template string can be changed in extension settings.

Default template:

    {artist} - {title}
    Album: {album}     ({playback_status})


Available tags:

- `{artist}` - Track artist
- `{title}` - Track title
- `{album}` - Album title
- `{playback_status}` - "Playing"/"Paused" status

Tags have to be enclosed in `{` and `}` braces.
If you want to include { or } in formatting string, use escaped form `{{` or `}}`.
Any unbalanced braces (unescaped) or unknown tag names will show an error (during displaying menu, not during defining the template in settings).

String can have more than two lines (it doesn't cause an error), but only first two lines will be displayed.