Usage
=====

First, import the module:

.. code:: python

   import sounddevice as sd

Playback
--------

Assuming you have a NumPy array named ``myarray`` holding audio data with a
sampling frequency of ``fs`` (in the most cases this will be 44100 or 48000
frames per second), you can play it back with `sounddevice.play()`:

.. code:: python

   sd.play(myarray, fs)

This function returns immediately but continues playing the audio signal in the
background.  You can stop playback with `sounddevice.stop()`:

.. code:: python

   sd.stop()

If you know that you will use the same sampling frequency for a while, you can
set it as default using `sounddevice.default.samplerate`:

.. code:: python

   sd.default.samplerate = fs

After that, you can drop the *samplerate* argument:

.. code:: python

   sd.play(myarray)

Recording
---------

To record audio data from your sound device into a NumPy array, use
`sounddevice.rec()`:

.. code:: python

   duration = 10.5  # seconds
   myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=2)

Again, for repeated use you can set defaults using `sounddevice.default`:

.. code:: python

   sd.default.samplerate = fs
   sd.default.channels = 2

After that, you can drop the additional arguments:

.. code:: python

   myrecording = sd.rec(int(duration * fs))

This function also returns immediately but continues recording in the
background.  In the meantime, you can run other commands.  If you want to check
if the recording is finished, you should use `sounddevice.wait()`:

.. code:: python

   sd.wait()

If the recording was already finished, this returns immediately; if not, it
waits and returns as soon as the recording is finished.

Alternatively, you could have used the *blocking* argument in the first place:

.. code:: python

   myrecording = sd.rec(duration * fs, blocking=True)

By default, the recorded array has the data type ``'float32'`` (see
`sounddevice.default.dtype`), but this can be changed with the *dtype* argument:

.. code:: python

   myrecording = sd.rec(duration * fs, dtype='float64')

Simultaneous Playback and Recording
-----------------------------------

To play back an array and record at the same time, use `sounddevice.playrec()`:

.. code:: python

   myrecording = sd.playrec(myarray, fs, channels=2)

The number of output channels is obtained from ``myarray``, but the number of
input channels still has to be specified.

Again, default values can be used:

.. code:: python

   sd.default.samplerate = fs
   sd.default.channels = 2
   myrecording = sd.playrec(myarray)

In this case the number of output channels is still taken from ``myarray``
(which may or may not have 2 channels), but the number of input channels is
taken from `sounddevice.default.channels`.

Device Selection
----------------

In many cases, the default input/output device(s) will be the one(s) you want,
but it is of course possible to choose a different device.
Use `sounddevice.query_devices()` to get a list of supported devices.
The same list can be obtained from a terminal by typing the command ::

   python3 -m sounddevice

You can use the corresponding device ID to select a desired device by assigning
to `sounddevice.default.device` or by passing it as *device* argument to
`sounddevice.play()`, `sounddevice.Stream()` etc.

Instead of the numerical device ID, you can also use a space-separated list of
case-insensitive substrings of the device name (and the host API name, if
needed).  See `sounddevice.default.device` for details.

.. code:: python

   import sounddevice as sd
   sd.default.samplerate = 44100
   sd.default.device = 'digital output'
   sd.play(myarray)

Callback Streams
----------------

Callback "wire" with `sounddevice.Stream`:

.. code:: python

   import sounddevice as sd
   duration = 5.5  # seconds

   def callback(indata, outdata, frames, time, status):
       if status:
           print(status)
       outdata[:] = indata

   with sd.Stream(channels=2, callback=callback):
       sd.sleep(int(duration * 1000))

Same thing with `sounddevice.RawStream`:

.. code:: python

   import sounddevice as sd
   duration = 5.5  # seconds

   def callback(indata, outdata, frames, time, status):
       if status:
           print(status)
       outdata[:] = indata

   with sd.RawStream(channels=2, dtype='int24', callback=callback):
       sd.sleep(int(duration * 1000))

.. note:: We are using 24-bit samples here for no particular reason
   (just because we can).

Blocking Read/Write Streams
---------------------------

Instead of using a callback function, you can also use the blocking methods
`sounddevice.Stream.read()` and `sounddevice.Stream.write()` (and of course the
corresponding methods in `sounddevice.InputStream`, `sounddevice.OutputStream`,
`sounddevice.RawStream`, `sounddevice.RawInputStream` and
`sounddevice.RawOutputStream`).
