Contributing
------------

If you find bugs, errors, omissions or other things that need improvement,
please create an issue or a pull request at
https://github.com/spatialaudio/python-sounddevice/.
Contributions are always welcome!

Instead of pip-installing the latest release from PyPI, you should get the
newest development version from Github_::

   git clone --recursive https://github.com/spatialaudio/python-sounddevice.git
   cd python-sounddevice
   python3 setup.py develop --user

.. _Github: https://github.com/spatialaudio/python-sounddevice/

This way, your installation always stays up-to-date, even if you pull new
changes from the Github repository.

If you prefer, you can also replace the last command with::

   python3 -m pip install --user -e .

... where ``-e`` stands for ``--editable``.

Whenever the file ``sounddevice_build.py`` changes (either because you edited it
or it was updated by pulling from Github or switching branches), you have to run
the last command again.

If you used the ``--recursive`` option when cloning, the dynamic libraries for
*macOS* and *Windows* should already be available.
If not, you can get the submodule with::

   git submodule update --init

If you make changes to the documentation, you can locally re-create the HTML
pages using Sphinx_.
You can install it and a few other necessary packages with::

   python3 -m pip install -r doc/requirements.txt --user

To create the HTML pages, use::

   python3 setup.py build_sphinx

The generated files will be available in the directory ``build/sphinx/html/``.

.. _Sphinx: http://sphinx-doc.org/
