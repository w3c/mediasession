# Media Session Standard

https://w3c.github.io/mediasession/

This standardization project aims to add support for media keys and audio focus to the Web. Media keys, like play, pause, fast forward and rewind, are found on keyboards, headsets, remote controls, and on lock screens of mobile devices.

## Explainer

The explainer of the MediaSession API can be found [here](explainer.md).

## Use cases

The use cases of the MediaSession API can be found [here](use_cases.md).

## Extensibility
Our goal is to provide developers with low-level primitives that both help explain the platform, while also allowing developers to build rich multimedia experiences that leverage media key events. Keeping to our commitment to the [extensible web manifesto](https://extensiblewebmanifesto.org/), we want to allow the media key events to be routed to wherever you need them in your web application. At the same time, we want to make sure that whatever solution we come up with is easy to use &ndash; by possibly extending existing HTML elements or APIs.

## Limitations
Access to media keys and lock screen UI will only be granted when audio playback begins, ensuring that audio focus is not taken from another application prematurely and that lock screen UI is only shown when it can be used. This matches the [iOS model](https://developer.apple.com/library/ios/documentation/EventHandling/Conceptual/EventHandlingiPhoneOS/Remote-ControlEvents/Remote-ControlEvents.html).

## Contribute

This spec is built using [Bikeshed](https://github.com/tabatkins/bikeshed).

Update `index.bs` and send a Pull Request with your changes. When your Pull Request will be merged, a new `index.html` will be generated. If you want to test locally, you can run `make` to generate `index.html` using [Bikeshed's web interface](https://api.csswg.org/bikeshed/). However, you should not send the `index.html` file in your Pull Request.

To run Bikeshed locally, [install Bikeshed](https://github.com/tabatkins/bikeshed/blob/prespec/docs/install.md) and then run `bikeshed spec` in the working directory.

Everyone is welcome to contribute! See the [CONTRIBUTING.md](CONTRIBUTING.md) file for practical licensing details for contributions.

## Code of conduct

We are committed to providing a friendly, safe and welcoming environment for all. Please read and
respect the [W3C Code of Conduct](https://www.w3.org/Consortium/cepc/).
