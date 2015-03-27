# Media Session API

A media session represents a source of media playback on the system. Typically an application needs only one session, but more fine-grained control is possible.

Note: This corresponds roughly to [audio focus on Android](http://developer.android.com/training/managing-audio/audio-focus.html) and [audio session on iOS](https://developer.apple.com/library/ios/documentation/Audio/Conceptual/AudioSessionProgrammingGuide/Introduction/Introduction.html).

When a media session becomes active, all other media sessions are either deactivated or interrupted, depending on kind of session.

```WebIDL
enum MediaSessionKind { "ambient", "default", "voice" };

enum MediaSessionState { "inactive", "active", "suspended" };

[Constructor(optional MediaSessionKind kind = "default")]
interface MediaSession : EventTarget {
    readonly attribute MediaSessionKind kind;
    readonly attribute MediaSessionState state;

    // Try to activate the session. The promise is rejected if the session is
    // suspended or would be immediately suspended if activated.
    Promise<void> activate();

    // Deactivate the session.
    Promise<void> deactivate();

    // events for state transitions
    attribute EventHandler onactive; // inactive -> active
    attribute EventHandler oninactive; // active/suspended -> inactive
    attribute EventHandler onsuspend; // active -> suspended
    attribute EventHandler onresume; // suspended -> active
};
```

## Handling media keys

An active media session is required in order to receive media key events.

Note: This corresponds roughly to [media session on Android](http://developer.android.com/training/managing-audio/audio-focus.html) and [remote control events on iOS](https://developer.apple.com/library/ios/documentation/EventHandling/Conceptual/EventHandlingiPhoneOS/Remote-ControlEvents/Remote-ControlEvents.html).

```WebIDL
partial interface MediaSession {
    attribute EventHandler onplay; // play/pause button pressed while inactive
    attribute EventHandler onpause; // play/pause button pressed while active
    attribute EventHandler onprevious; // previous track or rewind
    attribute EventHandler onnext; // next track or fast forward
};
```

### Example

In this example, a `MediaSession` is used to control a playlist.

```HTML
<audio controls></audio>
<script>
var audio = document.querySelector("audio");
var session = new MediaSession();
audio.session = session;

var tracks = [
    { src: "track1.ogg", title: "Intro" },
    { src: "track2.ogg", title: "A Song" },
    { src: "track3.ogg", title: "Outro" },
];

var selectedTrack = 0;
function selectTrack(index) {
    if (index < 0 || index >= tracks.length) {
        // do nothing, could also wrap around
        return;
    }
    audio.src = tracks[index].src;
    session.title = tracks[index].title;
    selectedTrack = index;
}

// ISSUE: This is going to be very boilerplatey, think about defaults.
session.addEventListener('play', function() {
    audio.play();
});

session.addEventListener('pause', function() {
    audio.pause();
});

session.addEventListener('previous', function() {
    selectTrack(selectedTrack - 1);
});

session.addEventListener('next', function() {
    selectTrack(selectedTrack + 1);
});

selectTrack(0);

// activate the session and then start playing
session.activate().then(function() {
    audio.play();
});
</script>
```

ISSUE: [Why can't keyboard events be used here?](https://github.com/whatwg/media-keys/issues/21).

## Providing lock screen controls

An active media session is required in order to get lock screen controls.

```WebIDL
partial interface MediaSession {
    attribute DOMString title;
    attribute DOMString poster;
    // TODO: figure out how to test support for and request additional buttons
};
```

## Integration with `AudioContext` and `HTMLMediaElement`

There are three ways in which `MediaSession` could be connected to `AudioContext` and `HTMLMediaElement`:
 1. An active `MediaSession` is required in order to start playing audio.
 2. Playing audio is required for a `MediaSession` to become active.
 3. Two-way coupling, such that beginning playback and becoming the active `MediaSession` is a transaction.

Every `AudioContext` or `HTMLMediaElement` could be associated with a `MediaSession`.

```WebIDL
partial interface AudioContext {
    attribute MediaSession session;
};
```

```WebIDL
partial interface HTMLMediaElement {
    attribute MediaSession session;
};
```

The behavior would be as follows for each case:
 1. Trying to play with an inactive session first tries to activate that session and then starts playing.
 2. Trying to activate a session which is not connected to any playing media fails with no further action.
 3. Like 1, but trying to begin playback would be the *only* way to activate a session, so `MediaSession.activate()` would not be needed.

ISSUE: [Figure out the coupling between audio focus/session, audio playback and remote control events](https://github.com/whatwg/media-keys/issues/9)
