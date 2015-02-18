# Media Session API

A `MediaSession` would have a set of `HTMLMediaElement`s or `AudioContext`s, and it is when one of the members in this set reaches a particular state (approximately when the `playing` event is fired in the case of media elements) that this `MediaSession` becomes the recipient of hardware keys. It would continue to receive these events as long as nothing else takes the "focus" away, but would also have a `.end()` or similar to explicitly release control over lock screen UI and similar.

By associating multiple audio-producing objects with a single `MediaSession`, we avoid the problem of handing "audio focus" between media elements in the multi-element playlist case.

Also, I would like for there to be a document-wide default `MediaSession` to which all media elements belong by default, and which gets its title from document.title or similar, explaining the automatic lock screen behavior iOS already has and Opera for Android's notification UI for ongoing media playback.

## Interface `MediaSession`
```WebIDL
enum MediaSessionState { "paused", "playing", /* maybe more */ };
typedef (HTMLMediaElement or AudioContext) MediaSessionMember;

interface MediaSession : EventTarget {
    readonly attribute MediaSessionState state;

    readonly attribute MediaSessionMember[] members;
    void addMember(MediaSessionMember member);
    void removeMember(MediaSessionMember member);

    void end(); // or inactivate() maybe

    // events to notify
    attribute EventHandler onactive; // session became the active one
    attribute EventHandler oninactive; // session is no longer active

    // events with default actions which can possible by preventDefault()'ed
    attribute EventHandler onplay; // forwards to members by default
    attribute EventHandler onpause; // forwards to members by default
    attribute EventHandler onprevious; // previous track
    attribute EventHandler onnext; // next track
    attribute EventHandler onstar; // maybe stuff like this that iOS has
};
```
