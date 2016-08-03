# Media Session Standard

https://wicg.github.io/mediasession/

This standardization project aims to add support for media keys and audio focus to the Web. Media keys, like play, pause, fast forward and rewind, are found on keyboards, headsets, remote controls, and on lock screens of mobile devices. Audio focus is the system which ensures that application do not play over each other and that only one application at a time responds to media key events. It allows one application to pause when another application begins playback, or to duck (lower volume) for a short notification.

## Use cases

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

Phones and tablets may have media controls on the lock screen. ([iOS](http://appadvice.com/appnn/2013/06/the-appadvice-ios-7-quick-pick-controlling-music-while-on-the-lock-screen), [Android](http://stackoverflow.com/questions/12168046/remote-control-client-for-android)) Applications may also have media controls in the notification area, which are very similar to lock screen controls but can be dismissed. ([Android](http://stackoverflow.com/questions/14508369/how-to-create-a-notification-similar-to-play-music-app-from-google))

The play/pause button should function like a keyboard's play/pause key. Where supported, the web application should be able to control:
* Whether rewind and fast forward buttons appear and their behavior.
* Title and subtitle, e.g. artist name and track title.
* Background image, e.g. album art.
* Any additional buttons, e.g. like/favorite.

### Audio Focus / Audio Session

The audio focus ([Android](http://developer.android.com/training/managing-audio/audio-focus.html)) or audio session ([iOS](https://developer.apple.com/library/ios/documentation/Audio/Conceptual/AudioSessionProgrammingGuide/Introduction/Introduction.html)) system is what controls access to media keys and lock screen UI. However, it also controls behavior when multiple applications compete for audio playback:
* While listening to music, start watching a movie instead. The music automatically pauses.
* While listening to music, a message is received. The music volume is lowered (i.e., "ducked") for the notification sound to be clearly heard.
* While listening to music, there is an incoming call. The music pauses while the call is ongoing and then resumes.
* While listening to a podcast, there is a message or incoming call. The podcast pauses, and eventually resumes playback slightly before where it paused, so that nothing is missed.
* Join a video chat in the browser. Any other audio playback on the system stops.

## Extensibility
Our goal is to provide developers with low-level primitives that both help explain the platform, while also allowing developers to build rich multimedia experiences that leverage media key events. Keeping to our commitment to the [extensible web manifesto](https://extensiblewebmanifesto.org/), we want to allow the media key events to be routed to wherever you need them in your web application. At the same time, we want to make sure that whatever solution we come up with is easy to use &ndash; by possibly extending existing HTML elements or APIs.

## Limitations
Access to media keys and lock screen UI will only be granted when audio playback begins, ensuring that audio focus is not taken from another application prematurely and that lock screen UI is only shown when it can be used. This matches the [iOS model](https://developer.apple.com/library/ios/documentation/EventHandling/Conceptual/EventHandlingiPhoneOS/Remote-ControlEvents/Remote-ControlEvents.html).

## Contribute

This spec is built using [Bikeshed](https://github.com/tabatkins/bikeshed).

Update `index.bs` and send a Pull Request with your changes. When your Pull Request will be merged, a new `index.html` will be generated. If you want to test locally, you can run `make` to generate `index.html` using [Bikeshed's web interface](https://api.csswg.org/bikeshed/). However, you should not send the `index.html` file in your Pull Request.

To run Bikeshed locally, [install Bikeshed](https://github.com/tabatkins/bikeshed/blob/prespec/docs/install.md) and then run `bikeshed spec` in the working directory.

Everyone is welcome to contribute! However, you need [join WICG](https://www.w3.org/community/wicg/) first and sign the [W3C Community Contributor License Agreement](https://www.w3.org/community/about/agreements/cla/).

## Code of conduct

We are committed to providing a friendly, safe and welcoming environment for all. Please read and
respect the [W3C Code of Conduct](https://www.w3.org/Consortium/cepc/).
