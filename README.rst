Play and Record Sound with Python
=================================

This Python_ module provides bindings for the PortAudio_ library and a few
convenience functions to play and record NumPy_ arrays containing audio signals.

Documentation:
   http://python-sounddevice.readthedocs.io/

Source code repository and issue tracker:
   https://github.com/spatialaudio/python-sounddevice/

License:
   MIT -- see the file ``LICENSE`` for details.

.. image:: https://badge.fury.io/py/sounddevice.svg
   :target: https://pypi.python.org/pypi/sounddevice/

.. image:: https://repology.org/badge/vertical-allrepos/python:sounddevice.svg
   :target: https://repology.org/metapackage/python:sounddevice

Requirements
------------

Python:
   Of course, you'll need Python_.
   Any version where CFFI (see below) is supported should work.
   If you don't have Python installed yet, you should get one of the
   distributions which already include CFFI and NumPy (and many other useful
   things), e.g. Anaconda_ or WinPython_.

pip/setuptools:
   Those are needed for the installation of the Python module and its
   dependencies.  Most systems will have these installed already, but if not,
   you should install it with your package manager or you can download and
   install ``pip`` and ``setuptools`` as described on the `pip installation`_
   page.
   If you happen to have ``pip`` but not ``setuptools``, use this command::

      python3 -m pip install setuptools --user

   To upgrade to a newer version of an already installed package (including
   ``pip`` itself), use the ``--upgrade`` flag.

CFFI:
   The `C Foreign Function Interface for Python`_ is used to access the C-API
   of the PortAudio library from within Python.  It supports CPython 2.6, 2.7,
   3.x; and is distributed with PyPy_.
   If it's not installed already, you should install it with your package
   manager (the package might be called ``python3-cffi`` or similar), or you can
   get it with::

      python3 -m pip install cffi --user

PortAudio library:
   The PortAudio_ library must be installed on your system (and CFFI must be
   able to find it).  Again, you should use your package manager to install it
   (the package might be called ``libportaudio2`` or similar).
   If you prefer, you can of course also download the sources and compile the
   library yourself.  If you are using Mac OS X or Windows, the library will be
   installed automagically with *pip* (see "Installation" below).

NumPy (optional):
   NumPy_ is only needed if you want to play back and record NumPy arrays.
   The classes `sounddevice.RawStream`, `sounddevice.RawInputStream` and
   `sounddevice.RawOutputStream` use plain Python buffer objects and don't need
   NumPy at all.
   If you need NumPy, you should install it with your package manager or use a
   Python distribution that already includes NumPy (see above).
   You can also install NumPy with ``pip``, but depending on your platform, this
   might require a compiler and several additional libraries::

      python3 -m pip install NumPy --user

.. _PortAudio: http://www.portaudio.com/
.. _NumPy: http://www.numpy.org/
.. _Python: https://www.python.org/
.. _Anaconda: https://www.anaconda.com/download/
.. _WinPython: http://winpython.github.io/
.. _C Foreign Function Interface for Python: http://cffi.readthedocs.io/
.. _PyPy: http://pypy.org/
.. _pip installation: https://pip.pypa.io/en/latest/installing/

Installation
------------

Once you have installed the above-mentioned dependencies, you can use pip
to download and install the latest release with a single command::

   python3 -m pip install sounddevice --user

If you want to install it system-wide for all users (assuming you have the
necessary rights), you can just drop the ``--user`` option.
If you have installed the module already, you can use the ``--upgrade`` flag to
get the newest release.

To un-install, use::

   python3 -m pip uninstall sounddevice

If you are using Windows, you can alternatively install one of the packages
provided at https://www.lfd.uci.edu/~gohlke/pythonlibs/#sounddevice.
The PortAudio library is also included in the package and you can get the rest
of the dependencies on the same page.

Usage
-----

First, import the module:

.. code:: python

   import sounddevice as sd

Playback
^^^^^^^^

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
^^^^^^^^^

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

   myrecording = sd.rec(duration * fs)

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
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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
^^^^^^^^^^^^^^^^

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
^^^^^^^^^^^^^^^^

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
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Instead of using a callback function, you can also use the blocking methods
`sounddevice.Stream.read()` and `sounddevice.Stream.write()` (and of course the
corresponding methods in `sounddevice.InputStream`, `sounddevice.OutputStream`,
`sounddevice.RawStream`, `sounddevice.RawInputStream` and
`sounddevice.RawOutputStream`).
