# Use Cases of the MediaSession API

Broadly, we want to support the following use cases:

### Keyboard media keys

Keyboards may have play/pause, stop, rewind and fast forward keys. ([Apple](http://cupertinotimes.com/mac-media-keys-fix/), [Corsair](http://benchmarkreviews.com/2006/corsair-vengeance-k70-mechanical-gaming-keyboard-ch-9000011-uk-review/3/))

* While watching a video or listening to audio in the background, pause and resume playback using the play/pause key.
* While watching a video playlist or listening to a music playlist, skip between videos/tracks using the rewind and fast forward keys.
* While listening to a podcast, skip backward and forward ~10 seconds using the rewind and fast forward keys.

### Headphone buttons

Headphones may have a multi-purpose button and volume buttons. ([Apple](http://store.apple.com/us/product/MD827LL/A/apple-earpods-with-remote-and-mic), [Samsung](http://www.samsung.com/us/mobile/cell-phones-accessories/EO-HS5303BESTA))

The headphone button should mostly function like a keyboard's play/pause key. Additionally:
* While watching a video, turn off the screen. The audio continues to play and can be paused and resumed with the headphone button.
* Double tap and other key sequences may follow platform-specific conventions. ([iPhone](http://www.cnet.com/how-to/ten-hidden-controls-of-the-iphone-headphones/))

### Lock screen and notification area

PCs, phones and tablets may have media controls on the lock screen. ([Windows](https://docs.microsoft.com/en-us/windows/uwp/audio-video-camera/integrate-with-systemmediatransportcontrols), [iOS](http://appadvice.com/appnn/2013/06/the-appadvice-ios-7-quick-pick-controlling-music-while-on-the-lock-screen), [Android](http://stackoverflow.com/questions/12168046/remote-control-client-for-android)) Applications may also have media controls in the notification area, which are very similar to lock screen controls but can be dismissed. ([Android](http://stackoverflow.com/questions/14508369/how-to-create-a-notification-similar-to-play-music-app-from-google))

The play/pause button should function like a keyboard's play/pause key. Where supported, the web application should be able to control:

* Whether rewind and fast forward buttons appear and their behavior.
* Title and subtitle, e.g. artist name and track title.
* Background image, e.g. album art.
* Any additional buttons, e.g. like/favorite.
