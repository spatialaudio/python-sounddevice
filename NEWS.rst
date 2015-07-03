Version 0.2.0 (2015-07-03):
 * support for wheels including a dylib for Mac OS X and DLLs for Windows.
   The code for creating the wheels is largely taken from PySoundFile_.
 * remove logging (this seemed too intrusive)
 * return callback status from `sounddevice.wait()` and add the new function
   `sounddevice.get_status()`
 * `sounddevice.playrec()`: Rename the arguments *input_channels* and
   *input_dtype* to *channels* and *dtype*, respectively

   .. _PySoundFile: https://github.com/bastibe/PySoundFile/

Version 0.1.0 (2015-06-20):
   Initial release.  Some ideas are taken from PySoundCard_.  Thanks to Bastian
   Bechtold for many fruitful discussions during the development of several
   features which *python-sounddevice* inherited from there.

   .. _PySoundCard: https://github.com/bastibe/PySoundCard/
