0.3.13 (2019-02-27):
 * Examples ``asyncio_coroutines.py`` and ``asyncio_generators.py``

0.3.12 (2018-09-02):
 * Support for the dylib from Anaconda

0.3.11 (2018-05-07):
 * Support for the DLL from ``conda-forge``

0.3.10 (2017-12-22):
 * Change the way how the PortAudio library is located

0.3.9 (2017-10-25):
 * Add `sounddevice.Stream.closed`
 * Switch CFFI usage to "out-of-line ABI" mode

0.3.8 (2017-07-11):
 * Add more ``ignore_errors`` arguments
 * Add `sounddevice.PortAudioError.args`
 * Add `sounddevice.CoreAudioSettings`

0.3.7 (2017-02-16):
 * Add `sounddevice.get_stream()`
 * Support for CData function pointers as callbacks

0.3.6 (2016-12-19):
 * Example application ``play_long_file.py``

0.3.5 (2016-09-12):
 * Add ``extra_settings`` option for host-API-specific stream settings
 * Add `sounddevice.AsioSettings` and `sounddevice.WasapiSettings`

0.3.4 (2016-08-05):
 * Example application ``rec_unlimited.py``

0.3.3 (2016-04-11):
 * Add ``loop`` argument to `sounddevice.play()`

0.3.2 (2016-03-16):
 * ``mapping=[1]`` works now on all host APIs
 * Example application ``plot_input.py`` showing the live microphone signal(s)
 * Device substrings are now allowed in `sounddevice.query_devices()`

0.3.1 (2016-01-04):
 * Add `sounddevice.check_input_settings()` and
   `sounddevice.check_output_settings()`
 * Send PortAudio output to ``/dev/null`` (on Linux and OSX)

0.3.0 (2015-10-28):
 * Remove `sounddevice.print_devices()`, `sounddevice.query_devices()` can be
   used instead, since it now returns a `sounddevice.DeviceList` object.

0.2.2 (2015-10-21):
 * Devices can now be selected by substrings of device name and host API name

0.2.1 (2015-10-08):
 * Example applications ``wire.py`` (based on PortAudio's ``patest_wire.c``)
   and ``spectrogram.py`` (based on code by Mauris Van Hauwe)

0.2.0 (2015-07-03):
 * Support for wheels including a dylib for Mac OS X and DLLs for Windows.
   The code for creating the wheels is largely taken from PySoundFile_.
 * Remove logging (this seemed too intrusive)
 * Return callback status from `sounddevice.wait()` and add the new function
   `sounddevice.get_status()`
 * `sounddevice.playrec()`: Rename the arguments *input_channels* and
   *input_dtype* to *channels* and *dtype*, respectively

   .. _PySoundFile: https://github.com/bastibe/SoundFile/

0.1.0 (2015-06-20):
   Initial release.  Some ideas are taken from PySoundCard_.  Thanks to Bastian
   Bechtold for many fruitful discussions during the development of several
   features which *python-sounddevice* inherited from there.

   .. _PySoundCard: https://github.com/bastibe/PySoundCard/
