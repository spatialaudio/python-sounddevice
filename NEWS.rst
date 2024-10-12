0.5.1 (2024-10-12):
 * Windows wheel: bundle both non-ASIO and ASIO DLLs, the latter can be chosen
   by defining the ``SD_ENABLE_ASIO`` environment variable

0.5.0 (2024-08-11):
 * Remove ASIO support from bundled DLLs (DLLs with ASIO can be manually selected)

0.4.7 (2024-05-27):
 * support ``paWinWasapiAutoConvert`` with ``auto_convert`` flag in `WasapiSettings`
 * Avoid exception in `PortAudioError`\ ``.__str__()``

0.4.6 (2023-02-19):
 * Redirect stderr with ``os.dup2()`` instead of CFFI calls

0.4.5 (2022-08-21):
 * Add ``index`` field to device dict
 * Require Python >= 3.7
 * Add PaWasapi_IsLoopback() to cdef (high-level interface not yet available)

0.4.4 (2021-12-31):
 * Exact device string matches can now include the host API name

0.4.3 (2021-10-20):
 * Fix dimension check in `Stream.write()`
 * Provide "universal" (x86_64 and arm64) ``.dylib`` for macOS

0.4.2 (2021-07-18):
 * Update PortAudio binaries to version 19.7.0
 * Wheel names are now shorter

0.4.1 (2020-09-26):
 * `CallbackFlags` attributes are now writable

0.4.0 (2020-07-18):
 * Drop support for Python 2.x
 * Fix memory issues in `play()`, `rec()` and `playrec()`
 * Example application ``play_stream.py``

0.3.15 (2020-03-18):
 * This will be the last release supporting Python 2.x!

0.3.14 (2019-09-25):
 * Examples ``play_sine.py`` and ``rec_gui.py``
 * Redirect ``stderr`` only during initialization

0.3.13 (2019-02-27):
 * Examples ``asyncio_coroutines.py`` and ``asyncio_generators.py``

0.3.12 (2018-09-02):
 * Support for the dylib from Anaconda

0.3.11 (2018-05-07):
 * Support for the DLL from ``conda-forge``

0.3.10 (2017-12-22):
 * Change the way how the PortAudio library is located

0.3.9 (2017-10-25):
 * Add `Stream.closed`
 * Switch CFFI usage to "out-of-line ABI" mode

0.3.8 (2017-07-11):
 * Add more ``ignore_errors`` arguments
 * Add `PortAudioError.args`
 * Add `CoreAudioSettings`

0.3.7 (2017-02-16):
 * Add `get_stream()`
 * Support for CData function pointers as callbacks

0.3.6 (2016-12-19):
 * Example application ``play_long_file.py``

0.3.5 (2016-09-12):
 * Add ``extra_settings`` option for host-API-specific stream settings
 * Add `AsioSettings` and `WasapiSettings`

0.3.4 (2016-08-05):
 * Example application ``rec_unlimited.py``

0.3.3 (2016-04-11):
 * Add ``loop`` argument to `play()`

0.3.2 (2016-03-16):
 * ``mapping=[1]`` works now on all host APIs
 * Example application ``plot_input.py`` showing the live microphone signal(s)
 * Device substrings are now allowed in `query_devices()`

0.3.1 (2016-01-04):
 * Add `check_input_settings()` and `check_output_settings()`
 * Send PortAudio output to ``/dev/null`` (on Linux and OSX)

0.3.0 (2015-10-28):
 * Remove ``print_devices()``, `query_devices()` can be used instead,
   since it now returns a `DeviceList` object.

0.2.2 (2015-10-21):
 * Devices can now be selected by substrings of device name and host API name

0.2.1 (2015-10-08):
 * Example applications ``wire.py`` (based on PortAudio's ``patest_wire.c``)
   and ``spectrogram.py`` (based on code by Mauris Van Hauwe)

0.2.0 (2015-07-03):
 * Support for wheels including a dylib for Mac OS X and DLLs for Windows.
   The code for creating the wheels is largely taken from the soundfile_ module.
 * Remove logging (this seemed too intrusive)
 * Return callback status from `wait()` and add the new function `get_status()`
 * `playrec()`: Rename the arguments *input_channels* and *input_dtype*
   to *channels* and *dtype*, respectively

   .. _soundfile: https://github.com/bastibe/python-soundfile/

0.1.0 (2015-06-20):
   Initial release.  Some ideas are taken from PySoundCard_.  Thanks to Bastian
   Bechtold for many fruitful discussions during the development of several
   features which *python-sounddevice* inherited from there.

   .. _PySoundCard: https://github.com/bastibe/PySoundCard/
