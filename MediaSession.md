# Media Session API

A media session represents a source of media playback on the system, typically an application although more fine-grained control is possible.

An active media session is required in order to receive events from media key events and lock screen media controls.

When a media session becomes active, all other media sessions are either deactivated or interrupted, depending on kind of session.

## The `MediaSession` Interface

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

    // events for media keys
    attribute EventHandler onplay; // play/pause button pressed while inactive
    attribute EventHandler onpause; // play/pause button pressed while active
    attribute EventHandler onprevious; // previous track or rewind
    attribute EventHandler onnext; // next track or fast forward

    // metadata for lock screen UI
    attribute DOMString title;
    attribute DOMString poster;
    // TODO: figure out how to test support for and request additional buttons
};
```

## Integration with `AudioContext` and `HTMLMediaElement`

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

When an `AudioContext` or `HTMLMediaElement` is connected to a `MediaSession`, starting playback will implicitly call `MediaSession.activate()`.

ISSUE: Should an active `MediaSession` be required to start playback? This could explain the [media playback restrictions in Blink](http://blog.foolip.org/2014/02/10/media-playback-restrictions-in-blink/), and the similar system in WebKit.

## Examples

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
