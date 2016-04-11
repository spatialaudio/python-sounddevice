Version 0.3.3 (2016-04-11):
 * Add ``loop`` argument to `sounddevice.play()`

Version 0.3.2 (2016-03-16):
 * ``mapping=[1]`` works now on all host APIs
 * Example application ``plot_input.py`` showing the live microphone signal(s)
 * Device substrings are now allowed in `sounddevice.query_devices()`

Version 0.3.1 (2016-01-04):
 * Add `sounddevice.check_input_settings()` and
   `sounddevice.check_output_settings()`
 * Send PortAudio output to ``/dev/null`` (on Linux and OSX)

Version 0.3.0 (2015-10-28):
 * Remove `sounddevice.print_devices()`, `sounddevice.query_devices()` can be
   used instead, since it now returns a `sounddevice.DeviceList` object.

Version 0.2.2 (2015-10-21):
 * Devices can now be selected by substrings of device name and host API name

Version 0.2.1 (2015-10-08):
 * Example applications ``wire.py`` (based on PortAudio's ``patest_wire.c``)
   and ``spectrogram.py`` (based on code by Mauris Van Hauwe)

Version 0.2.0 (2015-07-03):
 * Support for wheels including a dylib for Mac OS X and DLLs for Windows.
   The code for creating the wheels is largely taken from PySoundFile_.
 * Remove logging (this seemed too intrusive)
 * Return callback status from `sounddevice.wait()` and add the new function
   `sounddevice.get_status()`
 * `sounddevice.playrec()`: Rename the arguments *input_channels* and
   *input_dtype* to *channels* and *dtype*, respectively

   .. _PySoundFile: https://github.com/bastibe/PySoundFile/

Version 0.1.0 (2015-06-20):
   Initial release.  Some ideas are taken from PySoundCard_.  Thanks to Bastian
   Bechtold for many fruitful discussions during the development of several
   features which *python-sounddevice* inherited from there.

   .. _PySoundCard: https://github.com/bastibe/PySoundCard/
