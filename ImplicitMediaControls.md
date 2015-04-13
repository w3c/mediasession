# Implicit media focus, key binding, events and overrides

If we improve the default handling of HTML media within user agents and allow web developers to classify and differentiate between different kinds of media usage then web applications will gain powerful and overridable integration options to any attached hardware or software-based remote control interfaces.

By creating a strong binding between HTML media elements and remote control keys and interfaces, user agents would be able to:

a.) take advantage of an [implicit user opt-in and media focus mechanism](#sectionA) based around actively playing `HTMLMediaElement` content.

b.) provide [platform-specific default media key binding](#sectionB) against `HTMLMediaElement` objects.

c.) utilize [logical mappings](#sectionC) between `HTMLMediaElement` objects and connected remote control keys.

d.) provide [access to advanced media keys](#sectionD) through the same model.

e.) [implicitly reflect state changes](#sectionE) between in-page media content and media key interfaces.

f.) [implicitly provide media metadata](#sectionF) to remote control interfaces for display to the user.

g.) allow web developers to [override platform-specific media focus behavior](#sectionG) based on the kind of media content.

h.) provide [contextual remote control access](#sectionH) depending on the kind of media content.

i.) provide appropriate [platform-level interaction between different kinds of media content](#sectionI) being played within the user agent.

j.) enable web developers to [intercept remote control events to drive any other web content](#sectionJ) as required (e.g. Web Audio API content, Flash-based media players, slideshows and presentations).

---

## <a name="sectionA"></a>A. Granting implicit remote control access to media content

On mobile devices, when a `playing` event is fired toward any `HTMLMediaElement`-based object (i.e. &lt;video&gt; or &lt;audio&gt; elements) it will implicitly obtain OS-level _media focus_ and will now be the **focused media element**.

Only one HTML media element can hold _media focus_ at any given time on mobile (see [(B)](#sectionB) for desktop). If another HTML media element currently holds the _media focus_ then the user agent must actively pause that element before making the current element the _focused media element_.

Any HTML media element can re-gain _media focus_ whenever a `playing` event is fired toward that element (i.e. whenever `.play()` is called by in-page JavaScript or by the user via HTML media controls against that HTML media element).

## B. <a name="sectionB"></a>Platform-agnostic media focus handling

In mobile user agents the common approach is to allow only one HTMLMediaElement to play out at any given time. On such platforms, it is possible to implement the implicit media focus concept described in the previous section.

In desktop user agents, where the common approach is to allow multiple media elements to play over the top of each other by default, this default media focus behavior would not be enforced. Instead, desktop user agents would only respond to any provided [overrides for media focus behavior based on the _kind_ of media content in use](#sectionG) to provide access to media keys and other remote control interfaces.

## C. <a name="sectionC"></a>Logical key binding between remote control interfaces and HTML media content

When a HTML media element is the _focused media element_ (see [(A)](#sectionA) above) then it is possible to relay remote control events from connected hardware and software remote control interfaces directly toward HTML media elements.

For example, when the user presses the 'Play/Pause' button on their headphones, it is possible to translate that to a 'play' or 'pause' action against the currently _focused media element_.

## D. <a name="sectionD"></a>Hooking up advanced media key controls to HTML media content

Many remote control interfaces also provide 'Previous' and 'Next' controls that can be used to seek within the current track or skip between tracks.

Web applications do not currently have any way to access these media key events.

To handle these keys we propose firing `next` and `previous` events toward the _focused media element_ whenever these remote control interface keys are pressed. This then allows web developers to handle these events if they want to and respond appropriately by seeking within the current track, transitioning to the next track by changing the `.src` of the current _focused media element_ or, pass media focus to another HTML media element by calling '.play()' on that other element (thereby transferring media focus to that other element).

## E. <a name="sectionE"></a>Automatically reflecting state changes between in-page media content and remote control interfaces

By having a strong two-way binding between `HTMLMediaElement`-based content and remote control interfaces, we can reflect state changes from both the in-page media toward the remote control interfaces and vice-versa.

For example, if the user seeks within the current track within the web page, we can automatically reflect the current position within the track in all attached remote control interfaces.

Vice-versa, if the user seeks within the current track from the media control interface, we can apply that seek behaviour automatically to the in-page media.

If the web developer changes e.g. the 'title' attribute of a currently _focused media element_ we can also quickly reflect that in any media control interfaces as appropriate.

## F. <a name="sectionF"></a>Implicitly obtain metadata to use in remote control interfaces

If a _focused media element_ has a `title` attribute then that would be displayed in all connected remote control interfaces. If the `title` attribute of that element changes then that change would be automatically reflected in all connected remote control interfaces.

If a _focused media element_ does not have a `title` attribute then the user agent could fallback to using the web page's `title`, if available, or URL.

Other attributes of HTML media element such as `poster` or media IDv3 data could be exploited to provide additional metadata to display in remote control interfaces automatically.

All the metadata we need to display in remote control interfaces can be provided through HTML media elements today.

## G. <a name="sectionG"></a>Overriding default media focus behavior depending on the kind of HTML media content

We introduced the platform-specific behavior in [(A)](#sectionA) and [(B)](#sectionB).

When a mobile user agent is minimized or otherwise placed in the background AND it contains currently playing media then the default behavior should be to _pause_ the _focused media element_ content.

The user can easily resume playback of the _focused media element_ through the mobile OS's notification area or lock-screen controls.

There are situations in which this behavior is not ideal. If the user begins playback of music via their user agent then when the user agent is minimized a more suitable behavior would be to allow that music to continue playing.

Due to these use cases we would like to provide a simple way for web developers to markup their HTML media content to indicate to the user agent how it should interact with both media keys and other media that may or may not be playing out.

To this effect we would like to introduce the 'kind' attribute to HTMLMediaElement as it is explained [here](https://github.com/richtr/html-media-focus/issues/6).

The types of interactions that are enforced between these different kinds of media content are left to user agents as a design choice.

## H. <a name="sectionH"></a>Providing contextual remote control interface displays

Typically 'notification'-like media content should not interface with remote control interfaces or events (i.e. notification sounds are transient in nature and therefore do not require such features).

However, if the user is playing music, then we will want to display a [music interface](http://cloud.addictivetips.com/wp-content/uploads/2014/01/iOS-7-Lock-screen-music-controls.jpg).

If the web application triggers playback of an alarm then we would want to display an [alarm interface](https://modmyi.com/images/anthony/stopalarmios8banner.png).

If the web application is listening for network events and receives an incoming WebRTC call, then we would want to display a [ringer interface](https://lh4.ggpht.com/NMOdKMOJuMS0bO4IQR1JkAPwycyfCDeQMOaU6Ao8M89WiX5BX--TqZ9HYwD4-_ic4aY=h900). If the user answers the call they could be returned to the web application's interface (with the web application responsible for fully connection the call at this point). Rejecting the call would pause the media content and not redirect the user to the web application's interface.

If a web developer is able to describe the kind of media they want to play, the user agent can provide the most appropriate interface for users for that media.

## I. <a name="sectionI"></a>Enforcing logical interaction between different kinds of media content

If a web page begins playback of a short, transient notification sound then it would be incorrect to pause that media when the user agent is minimized or display a media control interface with which to resume or pause playback given the transient nature of notification sounds.

Notification-like media content therefore does not require any interaction with remote control events. However, it may be that a user agent would like to play notifications _over the top_ of any other currently playing media content, slightly lowering the volume of that other media content until the notification sound has finished playback. This concept is known as 'ducking'.

If a web developer is able to describe the kind of media they want to play, the user agent is able to enforce the most appropriate interaction between different media types depending on what would make the most sense to its users.

## J. <a name="sectionJ"></a>Intercepting remote control events to drive any other type of web content

Given that this proposal revolves entirely around media content, it would still be possible for web applications to intercept remote control events and re-purpose those events to drive any other web content they may have in their web page.

For example, by playing a client-side generated silent media file the web application would obtain access to remote control events through a dummy HTML media element. The events fired toward that object could then be intercepted to e.g. play or pause Flash or Web Audio based media. These events could also be used to control a slideshow or a presentation via any available remote control interfaces.

[This example project](https://github.com/richtr/universal-remote-control-access) demonstrates how a web application could intercept and re-purpose remote control events obtained via media content to drive any other in-page web content.

---
