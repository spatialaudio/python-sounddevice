Installation
============

First of all, you'll need Python_.
There are many distributions of Python available,
anyone where CFFI_ is supported should work.

You can get the latest ``sounddevice`` release from PyPI_ (using ``pip``).
But first, it is recommended to create a virtual environment
(e.g. using `python3 -m venv`__ or `conda create`__).
After activating the environment, the ``sounddevice`` module can be installed with::

   python -m pip install sounddevice

__ https://docs.python.org/3/library/venv.html
__ https://docs.conda.io/projects/conda/en/latest/user-guide/getting-started.html#creating-environments

If you have already installed an old version of the module in the environment,
you can use the ``--upgrade`` flag to get the newest release.
To un-install, use::

   python -m pip uninstall sounddevice

If you want to try the very latest development version of the ``sounddevice`` module,
have a look at the section about :doc:`contributing`.

If you install the ``sounddevice`` module with ``pip`` on macOS or Windows,
the PortAudio_ library will be installed automagically.
On other platforms, you might have to install PortAudio with your package
manager (the package might be called ``libportaudio2`` or similar).

.. note::

   If you install PortAudio with a package manager (including ``conda``),
   it will likely override the version installed with ``pip``.

The NumPy_ library is only needed if you want to play back and record NumPy arrays.
The classes `sounddevice.RawStream`, `sounddevice.RawInputStream` and
`sounddevice.RawOutputStream` use plain Python buffer objects and don't need
NumPy at all.
If needed -- and not installed already -- NumPy can be installed like this::

   python -m pip install numpy


ASIO Support
------------

Installing the ``sounddevice`` module with ``pip`` (on Windows)
will provide two PortAudio_ DLLs, with and without ASIO support.
By default, the DLL *without* ASIO support is loaded
(because of the problems mentioned in `issue #496`__).
To load the DLL *with* ASIO support, the environment variable ``SD_ENABLE_ASIO``
has to be set *before* importing the ``sounddevice`` module,
for example like this:

.. code:: python

    import os

    # Set environment variable before importing sounddevice. Value is not important.
    os.environ["SD_ENABLE_ASIO"] = "1"

    import sounddevice as sd

    print(sd.query_hostapis())

__ https://github.com/spatialaudio/python-sounddevice/issues/496

.. note::

    This will only work if the ``sounddevice`` module has been installed via ``pip``.
    This will not work with the ``conda`` package (see below).

.. note::

    This will not work if a custom ``portaudio.dll`` is present in the ``%PATH%``
    (as described in the following section).


Custom PortAudio Library
------------------------

If you want to use a different version of the PortAudio library
(maybe a development version or a version with different features selected),
you can rename the library to ``libportaudio.so`` (Linux)
or ``libportaudio.dylib`` (macOS) and move it to ``/usr/local/lib``.
On Linux, you might have to run ``sudo ldconfig`` after that,
for the library to be found.
On Windows, you can rename the library to ``portaudio.dll``
and move it to any directory in your ``%PATH%``.
In case of doubt you should create a fresh directory for your library
and add that to your ``PATH`` variable.


Alternative Packages
--------------------

If you are using the ``conda`` package manager (e.g. with miniforge_),
you can install the ``sounddevice`` module from the ``conda-forge`` channel::

   conda install -c conda-forge python-sounddevice

You can of course also use ``mamba`` if ``conda`` is too slow.

.. note::

   The PortAudio package on ``conda-forge`` doesn't have ASIO support,
   see https://github.com/conda-forge/portaudio-feedstock/issues/9.

There are also packages for several other package managers:

.. only:: html

   .. image:: https://repology.org/badge/vertical-allrepos/python:sounddevice.svg
      :target: https://repology.org/metapackage/python:sounddevice

.. only:: latex

   https://repology.org/metapackage/python:sounddevice

.. _PortAudio: http://www.portaudio.com/
.. _NumPy: https://numpy.org/
.. _Python: https://www.python.org/
.. _miniforge: https://github.com/conda-forge/miniforge
.. _CFFI: https://cffi.readthedocs.io/
.. _PyPI: https://pypi.org/project/sounddevice/
