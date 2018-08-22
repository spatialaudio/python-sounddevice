Installation
============

First of all, you'll need Python_.
Any version where CFFI_ is supported should work.
If you don't have Python installed yet, you should get one of the
distributions which already include CFFI and NumPy_ (and many other useful
things), e.g. Anaconda_ or WinPython_.

.. only:: html

   .. image:: https://anaconda.org/conda-forge/python-sounddevice/badges/version.svg
      :target: https://anaconda.org/conda-forge/python-sounddevice

If you are using the ``conda`` package manager (e.g. with Anaconda_ for
Linux/macOS/Windows), you can install the ``sounddevice`` module from the
``conda-forge`` channel::

   conda install -c conda-forge python-sounddevice

There are also packages for several other package managers:

.. only:: html

   .. image:: https://repology.org/badge/vertical-allrepos/python:sounddevice.svg
      :target: https://repology.org/metapackage/python:sounddevice

.. only:: latex

   https://repology.org/metapackage/python:sounddevice

If you are using Windows, you can alternatively install one of the packages
provided at https://www.lfd.uci.edu/~gohlke/pythonlibs/#sounddevice.
The PortAudio_ library is included in the package and you can get the rest
of the dependencies on the same page.

Note that some of the aforementioned packages may be out-of-date.
You can always get the newest ``sounddevice`` release from PyPI_
(using ``pip``).
If you want to try the latest development version, have a look at the section
about :doc:`CONTRIBUTING`.

.. only:: html

   .. image:: https://badge.fury.io/py/sounddevice.svg
      :target: https://pypi.org/project/sounddevice/

To install the latest release from PyPI, use::

   python3 -m pip install sounddevice --user

If you want to install it system-wide for all users (assuming you have the
necessary rights), you can just drop the ``--user`` option.
If you have installed the module already, you can use the ``--upgrade`` flag to
get the newest release.

To un-install, use::

   python3 -m pip uninstall sounddevice

If you install the ``sounddevice`` module with ``pip`` on macOS or Windows, the
PortAudio_ library will be installed automagically.
On other platforms, you might have to install PortAudio with your package
manager (the package might be called ``libportaudio2`` or similar).

You might also have to install CFFI_ (from a package called ``python3-cffi`` or
similar).

NumPy_ is only needed if you want to play back and record NumPy arrays.
The classes `sounddevice.RawStream`, `sounddevice.RawInputStream` and
`sounddevice.RawOutputStream` use plain Python buffer objects and don't need
NumPy at all.
If you need NumPy, you should install it with your package manager (from a
package named ``python3-numpy`` or similar) or use a Python distribution that
already includes NumPy (see above).
You can also install NumPy with ``pip``, but depending on your platform, this
might require a compiler and several additional libraries.

.. _PortAudio: http://www.portaudio.com/
.. _NumPy: http://www.numpy.org/
.. _Python: https://www.python.org/
.. _Anaconda: https://www.anaconda.com/download/
.. _WinPython: http://winpython.github.io/
.. _CFFI: http://cffi.readthedocs.io/
.. _PyPI: https://pypi.org/project/sounddevice/
