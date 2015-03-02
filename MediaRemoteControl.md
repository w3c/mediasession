## MediaRemoteControl - Mozilla's proposal  

This document is intended solely for discussion as proposed API for addressing the use cases outlined in the [README](REAMDME.md). 

```IDL
[Constructor]
interface MediaRemoteControl: EventTarget {
  attribute EventHandler onremotekey;
  
  // This attribute is used to see if the play/pause event has been received correct.
  attribute boolean mediaActive;
  
  // An image to show when the device is locked.
  attribute MediaImage mediaImage;

  // Extra info to show.
  attribute DOMString mediaTitle;
  attribute DOMString mediaDuration;
  // other attributes.
};

typedef (DOMString or URL or Blob or HTMLImageElement or HTMLCanvasElement or HTMLVideoElement) MediaImage;

interface RemoteKeyEvent: Event {
  readonly attribute RemoteKeyEventType detail;
};

dictionary RemoteKeyEventInit: EventInit {
  RemoteKeyEventType detail = "play";
};

enum RemoteKeyEventType {
  "play", "pause", "playpause", "next", "previous",
  // possibly other codes
};
```
### Usage

```JS
var controller = new MediaRemoteControl();
controller.mediaTitle = "Maurice Ravel - Piano Concerto for the left hand"
controller.onremotekey = function (e) {
  switch (e.detail) {
  case "play":
    // ...
    break;
  case "pause":
    // ...
    break;
  }
};

```
 
### Notes
 
In the future we may be able to extend MediaRemoteControl to allow the application to provide some information about the currently playing track, such as the title, the picture, etc. 
That will enable us to build soft media controls on the lockscreen for example similar to the way that iOS and Android do.
 
We also need the webapp send information about if it's currently playing or not, so that the platform knows if it should display a "play" or a "pause" button on a software keyboard or a widget. This can also be useful to enable the platform to display playing-status next to song name etc. This might also enable us to dispatch the "play" or "pause" event rather than the "playpause" event.
