# Media Session - Security and Privacy Questionnaire

This document answers the [W3C Security and Privacy
Questionnaire](https://www.w3.org/TR/security-privacy-questionnaire/) for the
Media Session specification.

Last Update: 2017-01-05

**Does this specification deal with personally-identifiable information?**

No.

**Does this specification deal with high-value data?**

No.

**Does this specification introduce new state for an origin that persists across
browsing sessions?**

No.

**Does this specification expose persistent, cross-origin state to the web?**

No.

**Does this specification expose any other data to an origin that it doesn’t
currently have access to?**

This specification introduces new inputs for a website via the Media Session
Actions. These new inputs are not new data but can be used to discover user's
interaction with the device. The user agents should only trigger the action
handler when a website's Media Session is the active media session, thus forcing
a website to play something in order to be able to receive these new inputs.

**Does this specification enable new script execution/loading mechanisms?**

No.

**Does this specification allow an origin access to a user’s location?**

No.

**Does this specification allow an origin access to sensors on a user’s
device?**

No.

**Does this specification allow an origin access to aspects of a user’s local
computing environment?**

The new inputs mentioned above can come from a user agent UI component or
hardware components. For example, some devices have hardware media keys, some
users may have a headset or other devices that can control media.
Implementations of the specification should use these inputs and a malicious
website might try to discover user's local computing environment trough this
information. The specification does not advertize the source of the input so a
website will not be able to differentiate an action coming from the user agent
UI, the device hardware media keys or another device.

**Does this specification allow an origin access to other devices?**

No.

**Does this specification allow an origin some measure of control over a user
agent’s native UI?**

The MediaMetadata exposed by this specification are meant to be used by the user
agent to customize any UI it might build related to media playback. In addition,
it is expected to pass these information to the platform in order for native UI
to be customized.

**Does this specification expose temporary identifiers to the web?**

No.

**Does this specification distinguish between behavior in first-party and
third-party contexts?**

The specification does not have different behavior in first-party and
third-party contexts but allows the user agent to disable the feature for third-party contexts.

**How should this specification work in the context of a user agent’s
"incognito" mode?**

The specification does not normative requirements for incognito mode but offers
recommendations with regards to user's privacy in the [Security and Privacy
Considerations section](https://w3c.github.io/mediasession/index.html#security-privacy-considerations).

**Does this specification persist data to a user’s local device?**

No.

**Does this specification have a "Security Considerations" and
"Privacy Considerations" section?**

Yes.

**Does this specification allow downgrading default security characteristics?**

No.
