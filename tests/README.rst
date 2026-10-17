Synthetic ALSA tests
===================

These Linux tests exercise sounddevice and the real PortAudio ALSA backend
using null and file PCMs. No microphone or sound card is needed.
Run them in a fresh Python process so the isolated ALSA configuration is set
before PortAudio initialization. The fixture does not include system or user
ALSA configuration and restores the environment when the test session ends.

Install PortAudio and ALSA plugins (Debian/Ubuntu)::

    sudo apt-get install libportaudio2
    python -m pip install . pytest numpy
    python -m pytest -q tests

The temporary directory contains a deterministic input file and ALSA config.
It is removed at the end of the session. Non-Linux runs skip these tests;
missing ALSA support on Linux fails rather than silently skipping coverage.

The tests cover direct input/output/duplex, exact input bytes, close/reopen,
invalid parameters, settings lifetime, default overrides and existing indexed
and named selection. They do not validate hardware identity, physical capture,
hotplug, real-time scheduling or a negotiated hardware buffer size.

The raw-stream tests require only pytest and sounddevice. The convenience API
test uses NumPy and reports a skip when NumPy is unavailable (including the
PyPy CI jobs). CPython CI installs NumPy and exercises that test too.

ALSA_CONFIG_PATH cannot represent spaces or colons in its configuration path.
If the process temporary directory contains either, the fixture uses /tmp.
