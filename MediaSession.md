# Media Session API

A media session is required in order to recieve events from media key events and lock screen media controls. Each session can have one or several `AudioContext` or `HTMLMediaElement` objects as its members, and at least one of these must reach a playing state for the session to become active.

When a session has only one member, many of the events fired on it have a default action that acts on that single member. When there are multiple members, event handlers must be used to implement the desired behavior, as there is no sane default.

ISSUE: What measures should be taken to guarantee that pausing works even for a misbehaving user of `MediaSession`?

## The `MediaSession` Interface

```WebIDL
enum MediaSessionState { "idle", "playing", "paused", "ducking", "suspended" };
typedef (HTMLMediaElement or AudioContext) MediaSessionMember;

[Constructor()]
interface MediaSession : EventTarget {
    readonly attribute MediaSessionState state;

    // the objects which have this session as object.session
    readonly attribute MediaSessionMember[] members;

    // events with default actions when preventDefault() is not called
    attribute EventHandler onidle; // * -> idle
    attribute EventHandler onplay; // idle/paused -> playing
    attribute EventHandler onpause; // playing -> paused
    attribute EventHandler onduckstart; // playing -> ducking
    attribute EventHandler onduckend; // ducking -> playing
    attribute EventHandler onsuspend; // playing -> suspended
    attribute EventHandler onresume; // suspended -> playing

    // events with no default action
    attribute EventHandler onprevious; // previous track or rewind
    attribute EventHandler onnext; // next track or fast forward

    // metadata for lock screen UI
    attribute DOMString title;
    attribute DOMString poster;
    // TODO: figure out how to test support for and request additional buttons

    // end the media session, transitioning it to the idle state
    void end();
};
```

## Extensions to the `HTMLMediaElement` Interface

```WebIDL
partial interface HTMLMediaElement {
    attribute MediaSession session;
};
```

## Extensions to the `AudioContext` Interface

```WebIDL
partial interface AudioContext {
    attribute MediaSession session;
};
```

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

// default actions used for all events that have them

session.addEventListener('previous', function() {
    selectTrack(selectedTrack - 1);
});

session.addEventListener('next', function() {
    selectTrack(selectedTrack + 1);
});

selectTrack(0);
audio.autoplay = true; // session will become active if/when audio plays
</script>
```
