# Media Keys and Audio Focus/Session
This standardization project aims to add support for media keys to the Web, e.g. play, pause, fast-forward, rewind and volume. Media keys include hardware keys found on keyboards, headsets, remote controls, and software keys found on lock-screens of mobile devices.

Only one application at a time can be the recipient of media keys, and access is mediated by a system of [Audio Focus](http://developer.android.com/training/managing-audio/audio-focus.html) or [Audio Sessions](https://developer.apple.com/library/prerelease/ios/documentation/AVFoundation/Reference/AVAudioSession_ClassReference/index.html). Where appropriate, this also allows applications to pause when another application begins playback, or to duck (lower volume) for a short notification.

## What are we enabling?

Broadly, we want to support the following use cases:

### Media players
Allow a web application to register itself as a "media player". This will allow users to open their favorite music or video site, choose the media they want to listen to, and then have media key events routed to that web application. And yeah, this includes controlling media playback with buttons on a headset - even BlueTooth ones!

Users can then put a web application in the background (e.g., by opening a new tab), but allowing the web application to still respond to play, pause, fast-forward, and rewind media-key events.

Imagine also being able to play/pause movies you are watching from the web using a remote control. No need to get up an hit the space-bar anymore! :)

### System integration
Allow web applications to integrate with system media players, such as the one on iOS's lock screen. This will allow the software buttons on the lock screen to control the media playback. We also want to enable the ability to seek media.

Further, we want to make sure cover art, as well as other media-related metadata, shows up where appropriate - to provide the richest media control experience possible on any OS.

## Extensibility
Our goal is to provide developers with low-level primitives that both help explain the platform, while also allowing developers to build rich multimedia experiences that leverage media-key events. Keeping to our commitment to the [extensible web manifesto](https://extensiblewebmanifesto.org/), we want to allow the media-key events to be routed to wherever you need them in your web application. At the same time, we want to make sure that whatever solution we come up with is easy to use - by possibly extending existing HTML elements or APIs.

## Limitations
Access to media keys and lock screen UI will only be granted when audio playback begins, ensuring that audio focus is not taken from another application prematurely and that lock screen UI is only shown when it can be used. This matches the [iOS model](https://developer.apple.com/library/ios/documentation/EventHandling/Conceptual/EventHandlingiPhoneOS/Remote-ControlEvents/Remote-ControlEvents.html).

## Contribute
Everyone is welcome to contribute! However, by contributing you are agreeing to the [CC0 license](LICENSE).
