# MediaSession API Explained

## Objectives

People consume a lot of media (audio/video) and the Web is one of the primary
means of consuming this type of content. However, media on the web does not
integrate well with the platform. The MediaSession API helps closing the gap
between the web and native with a particular focus on mobile.

### Allowing pages to specify the currently playing media metadata

As many websites provide media content (eg. a video or audio clip) , they may
want to let the user know what media is currently playing (which is called
**media metadata**). Some sites (YouTube, Soundcloud, etc.) change the page
title to display this info. This work around has limitations when integrating
with the platform, for example there is no way to specify rich metadata like
album title, artist name or album art which can be displayed in platform UI.

The MediaSession API gives pages the ability to specify the metadata of the
currently playing media. The metadata will be passed to the platform, and can be
displayed in media centers, notification, device lockscreen etc. The user then
can observe what is currently playing. Here are some screenshots of
notification, control center and lockscreen for music & podcast applications
take on Android and iOS:

![Screenshots](images/screenshots.png)

### Allowing pages to respond to media controls

Many platforms provide interfaces for native app developers to respond to media
controls, which come from headset buttons, keyboard media buttons, media
centers, etc. It will improve the user experience significantly if web pages can
respond to these controls, especially for commands such as "play/pause",
"previous/next track" and "seek back/forward".

The MediaSession API gives pages the ability to respond to platform media
controls. By implementing the API, the user agent will act as a proxy and
pass the media controls to web pages, so that the pages can perform
corresponding actions.

For example, a podcast website can tell the user agent that it wants to receive
"seek forward/backward" commands, and when the commands are received, the
website changes the playback position accordingly. A music website can tell the
user agent that it wants to receive "previous/next track" commands, so that it
can switch tracks when these commands are received.

## API design

We want to achieve the two objectives in the same API because media metadata and
media controls are usually bonded together at least with regards to UI elements.
It is intuitive that a user to control the media whose metadata is displayed on
platform UI. On Android, the
[MediaSession class](https://developer.android.com/reference/android/media/session/MediaSession.html)
both handles media metadata and media controls, while on iOS,
[MPNowPlayingInfoCenter](https://developer.apple.com/library/ios/documentation/MediaPlayer/Reference/MPNowPlayingInfoCenter_Class/)
handles media metadata and
[MPRemoteCommandCenter](https://developer.apple.com/library/ios/documentation/MediaPlayer/Reference/MPRemoteCommandCenter_Ref/)
handles media controls but they are both singletons per application. Besides, it
is still doable if the page truly wants media metadata without media controls or
vice versa.

### The MediaSession interface

The `MediaSession` object is the main interface for this API, which looks like
the following:

```javascript
interface MediaSession : EventTarget {
    attribute MediaMetadata? metadata;

    attribute EventHandler onplay;
    attribute EventHandler onpause;
    attribute EventHandler onplaypause;
    attribute EventHandler onprevioustrack;
    attribute EventHandler onnexttrack;
    attribute EventHandler onseekbackward;
    attribute EventHandler onseekforward;
    ...
};
```

### The `MediaMetadata` interface

A `MediaMetadata` object can contain media metadata like title, artist, album
and album art. To set the metadata for a `MediaSession`, the page should create
a `MediaMetadata` object and assign it to a `MediaSession` object:

```javascript
// Let |session| be a MediaSession object
session.metadata = new MediaMetadata(/* MediaMetadata constructor */);
```

The `MediaMetadata` interface generally looks like (details are omitted):

```javascript
[Constructor=...]
interface MediaMetadata {
    attribute DOMString title;
    attribute DOMString artist;
    attribute DOMString album;
    attribute MediaImage artwork;  // Omitting MediaImage details
};
```

### Media controls

**Note** The API for media controls is still under development and may not be
stable.

The API for media controls should work as follows:

* The page registers event handlers for media control actions. A page
  registering an event handler for a media control action implies it supports
  that action.
* The user agent displays on UI for those controls (if applicable) and registers
  callbacks for those controls to the platform (if applicable).
* When the user initiates media control actions through UI or platform
  facilities, the user agent forwards the media control action to the page by
  calling the corresponding handler.

It is up to the user agent to decide which controls to show for in the UI and
register listeners to the platform. This may vary depending on UI concerns and
platform capabilities.

The user agent may have fallback behavior for some actions. There might be
useful in several use cases where the page wants to use or override the default
fallback behavior. The page can call `preventDefault()` in the event handler to
avoid the fallback behavior.

**Note** A possible issue with the above solution is that the user agent cannot
  know whether a event handler has `preventDefault()` until it calls the
  handler. After it's executed, the event handler may already run some steps,
  while the user agent can hardly know what steps are executed. Then the user
  agent may see `preventDefault()` is not called and do some fallback behavior.
  Suppose the user agent has a fallback `seekforward` implementation, and a page
  also does change the playback position for `seekforward`, then the playback
  position will be forwarded twice. This might end up with pages calling
  `preventDefault()` every time.

**Note** Websites might ignore some media control actions, especially
  "pause". In this case we might want to intervene these actions in the user
  agent or the platform. Another option is to handle these actions in the user
  agent and not exposing to the page at all. This is still an open question. See
  https://github.com/WICG/mediasession/issues/69

For action `play` and `pause`, the user agent need to use its best guess to
decide whether the page is playing or paused. We are considering add a boolean
attribute `playbackState` to let the page tell the playback state correctly. In
many cases, `play` and `pause` share the same media button. When the button is
pressed, the user agent should fire `pause` action when the page is playing and
fire `play` when the page is paused.

**Note** It is still an open question whether we need action `playpause`. The
  difference between `play`+`pause` and `playpause` is where the playback is
  decided. For `playpause`, it is decided by the page. For `play`+`pause`, it is
  decided by the user agent, but the page could possibly tell the playback state
  via a new attribute `playbackState`. See
  https://github.com/WICG/mediasession/issues/141

Here's an example for media controls:

```
// Suppose |audio| is an audio element and |session| is a MediaSession object.
session.onplay = function() {
    preventDefault();
    audio.play();
};

session.onpause = function() {
    preventDefault();
    audio.pause();
};

```

### `MediaSession` routing

#### Tab-level `MediaSession` routing

It usually makes more sense to display the media metadata of one page and let
only that page respond to media control actions than doing that for multiple
pages at the same time. Since multiple tabs can have `MediaSession` objects, the
user agent should have a routing mechanism to select one `MediaSession`. The
media metadata of the selected `MediaSession` will be passed to the platform for
UI display, and all media control actions are routed to that `MediaSession`. The
user agent should give control to the page or component that is currently
playing the most meaningful media to the user. If the AudioFocus API (see
[below](#sec-audiofocus-api)) is being used, it is defined by the
API. Otherwise, the user agent should route `MediaSession` based on platform
conventions and the preferred user experience.

#### Frame-level `MediaSession` routing

Another issue of `MediaSession` routing is how to select a `MediaSession` object
inside a tab, since `MediaSession` can both exist in the top-level frame and
child frames. When there are multiple frames having a `MediaSession` object, the
UA should decide which frame is playing the media content which is the most
meaningful to the user.

It is still an open question which `MediaSession` should be routed. For example,
the user plays a embedded YouTube video on Facebook, and YouTube sets the album
art to a YouTube logo, the user will be confused if the platform UI shows an
YouTube image, while it actually comes from Facebook. On the opposite, if a
website has an embedded music player, it might want to show the metadata from
the embedded music player, and let it respond to media control actions.

Since this is an UX decision, we need UA feedback to decide the default behavior
in the spec. Currently, it is up to the UA to decide.

### `MediaSession` as a global instance or a user-constructible object?

It is an open question that we make `MediaSession` a global instance or
user-constructible, the discussions are as follows:

#### `MediaSession` as a global instance (current spec)

If we consider each page as an application, it is straightforward that each page
has only one `MediaSession`, and the page takes full responsibility of setting
the media metadata and responds to media control actions. In this way, we can
make `MediaSession` a global object, and it is not user-constructible. For this
we provide a partial interface to the Navigator object:

```javascript
partial interface Navigator {
  readonly attribute MediaSession? mediaSession;
};
```

In this solution, the top-level frame and each child frame will have its own
`MediaSession` object, and the user agent should decide to select the
`MediaSession` from which frame to select. The top-level frame `MediaSession` is
preferred.

The advantage of this solution is very simple and easy to use, while the
disadvantage is that it may lack some flexibility, and there might be race
issues when the metadata is set in multiple places.

#### `MediaSession` as a user-constructible object (alternative spec)

A more flexible solution is to make `MediaSession` a user-constructible
object. `MediaSession`s can be activated and deactivated, and they can override
each other. In this way, the `MediaSession` interface will look like this:

```javascript
[Constructor()]
interface MediaSession {
    attribute MediaMetadata? metadata;
    // Omitting media control APIs

    Promise<void> activate();
    void deactivate();
    readonly attribute boolean   active;
    attribute EventHandler       onactivationchange;
};
```

The page can have multiple `MediaSession`s that exist at the same time, and it
needs to activate/deactivate them to indicate which one is in use. There will be
races if multiple `MediaSession`s are active at the same time, and the user
agent should decide which one to use (preferably the latest one becoming
active). Note that all this is within a page (tab), and does not conflict with
`MediaSession` routing.

An example is that suppose a video website plays a pre-roll ad before a video
plays, it can create one `MediaSession` for the video and one for the ad. The
page associates the `MediaSession`s to the video/ad state so that the
corresponding `MediaSession` is only active when the video/ad is playing.

The advantage of this solution is that we can obtain better composability with
other objects, especially AudioFocusEntry (from the AudioFocus API) objects. The
lifetime of the `MediaSession`s will be linked to these objects and they can be
activated/deactivated automatically when the associated objects start/stop
playback.

The disadvantage of this solution is that it might make the API complex to use,
and there are still race issues websites need to take care. Also, which is more
important, if the user agent does not have an automatic activation mechanism for
`MediaSession` (for example the AudioFocus API is not implemented), the benefit
will be very few since the solution is essentially equivalent to having multiple
`MediaMetadata` objects and setting different metadata to the global
`MediaSession` instance.

## Open questions

Here is a summary of the open questions mentioned above.

* What should we do if the page ignores some important media control handlers such
  as "pause"?
* Making `MediaSession` a global instance or a user-constructible object?
* Letting iframes use `MediaSession` or not?

## <a name="sec-audiofocus-api"></a>The AudioFocus API

The MediaSession API previously has an audio focus managing mechanism. We moved
audio focus managing into a separate API called AudioFocus API, which is still
work in progress. The reason for moving the AudioFocus API out are as follows:

* The AudioFocus API is less useful, and the current behavior is usually fine
  for rich media.
* The AudioFocus API is less mature but much more complex with a number of
  issues.
    * The AudioFocus API has possible compatibility issues with different
      platform.
    * WebAudio, WebRTC and plugins (e.g. Flash) are audio-producing, but they
      have a different model than media elements.
    * If some websites do not use the AudioFocus API, a good fallback behavior
      still needs to be investigated.

In general, the AudioFocus API improves audio mixing between web pages and
native applications on the platform. The AudioFocus API will provide
AudioFocusEntry interface. A web page can create AudioFocusEntry objects
specifying how they should be mixed with other AudioFocusEntrys or native
applications. The page can then adds audio-producing objects to the
AudioFocusEntry, and it needs to request audio focus when it wants to produce
audio and abandon audio focus when playback stops. The user agent will then
handle the audio mixing between web pages and native applications.

The AudioFocus API can interact with the MediaSession API in `MediaSession`
routing. It will also help in automatic `MediaSession` activation/deactivation
as well for the "`MediaSession` as a user-constructible object" solution.
