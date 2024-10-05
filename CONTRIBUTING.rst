Contributing
============

If you find bugs, errors, omissions or other things that need improvement,
please create an issue or a pull request at
https://github.com/spatialaudio/python-sounddevice/.
Contributions are always welcome!


Reporting Problems
------------------

When creating an issue at
https://github.com/spatialaudio/python-sounddevice/issues,
please make sure to provide as much useful information as possible.

You can use Markdown formatting to show Python code, e.g. ::

   I have created a script named `my_script.py`:

   ```python
   import sounddevice as sd

   fs = 48000
   duration = 1.5

   data = sd.rec(int(duration * fs), channels=99)
   sd.wait()
   print(data.shape)
   ```

Please provide minimal code
(remove everything that's not necessary to show the problem),
but make sure that the code example still has everything that's needed to run it,
including all ``import`` statements.

You should of course also show what happens when you run your code, e.g. ::

   Running my script, I got this error:

   ```
   $ python my_script.py 
   Expression 'parameters->channelCount <= maxChans' failed in 'src/hostapi/alsa/pa_linux_alsa.c', line: 1514
   Expression 'ValidateParameters( inputParameters, hostApi, StreamDirection_In )' failed in 'src/hostapi/alsa/pa_linux_alsa.c', line: 2818
   Traceback (most recent call last):
     File "my_script.py", line 6, in <module>
       data = sd.rec(int(duration * fs), channels=99)
   ...
   sounddevice.PortAudioError: Error opening InputStream: Invalid number of channels [PaErrorCode -9998]
   ```

Please remember to provide the full command invocation and the full output.
You should only remove lines of output when you know they are irrelevant.

You should also mention the operating system and host API you are using
(e.g. "Linux/ALSA" or "macOS/Core Audio" or "Windows/WASAPI").

If your problem is related to a certain hardware device,
you should provide the list of devices as reported by ::

   python -m sounddevice

If your problem has to do with the version of the PortAudio library you are using,
you should provide the output of this script::

   import sounddevice as sd
   print(sd._libname)
   print(sd.get_portaudio_version())

If you don't want to clutter the issue description with a huge load of gibberish,
you can use the ``<details>`` HTML tag to show some content only on demand::

   <details>

   ```
   $ python -m sounddevice
     0 Built-in Line Input, Core Audio (2 in, 0 out)
   > 1 Built-in Digital Input, Core Audio (2 in, 0 out)
   < 2 Built-in Output, Core Audio (0 in, 2 out)
     3 Built-in Line Output, Core Audio (0 in, 2 out)
     4 Built-in Digital Output, Core Audio (0 in, 2 out)
   ```

   </details>


Development Installation
------------------------

Instead of pip-installing the latest release from PyPI_, you should get the
newest development version (a.k.a. "master") from Github_::

   git clone --recursive https://github.com/spatialaudio/python-sounddevice.git
   cd python-sounddevice
   python -m pip install -e .

.. _PyPI: https://pypi.org/project/sounddevice/
.. _Github: https://github.com/spatialaudio/python-sounddevice/

This way, your installation always stays up-to-date, even if you pull new
changes from the Github repository.

Whenever the file ``sounddevice_build.py`` changes (either because you edited it
or it was updated by pulling from Github or switching branches), you have to run
the last command again.

If you used the ``--recursive`` option when cloning, the dynamic libraries for
*macOS* and *Windows* should already be available.
If not, you can get the submodule with::

   git submodule update --init


Building the Documentation
--------------------------

If you make changes to the documentation, you can locally re-create the HTML
pages using Sphinx_.
You can install it and a few other necessary packages with::

   python -m pip install -r doc/requirements.txt

To (re-)build the HTML files, use::

   python -m sphinx doc _build

The generated files will be available in the directory ``_build/``.

If you additionally install sphinx-autobuild_,
you can run Sphinx automatically on any changes
and conveniently auto-reload the changed pages in your browser::

   python -m sphinx_autobuild doc _build --open-browser

.. _Sphinx: https://www.sphinx-doc.org/
.. _sphinx-autobuild: https://github.com/executablebooks/sphinx-autobuild
