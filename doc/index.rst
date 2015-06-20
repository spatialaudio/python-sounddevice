.. default-role:: py:obj

.. include:: ../README.rst

.. include:: ../CONTRIBUTING.rst

.. default-role::

API Documentation
-----------------

.. automodule:: sounddevice
   :members:
   :undoc-members:
   :exclude-members: RawInputStream, RawOutputStream, RawStream,
                     InputStream, OutputStream, Stream,
                     CallbackFlags, CallbackStop, CallbackAbort, PortAudioError

.. autoclass:: Stream
   :members:
   :undoc-members:
   :inherited-members:

.. autoclass:: InputStream

.. autoclass:: OutputStream

.. autoclass:: RawStream
   :members: read, write

.. autoclass:: RawInputStream

.. autoclass:: RawOutputStream

.. autoclass:: CallbackFlags
   :members:

.. autoclass:: CallbackStop

.. autoclass:: CallbackAbort

.. autoclass:: PortAudioError

.. only:: html

   Index
   -----
 
   :ref:`genindex`

Version History
---------------

.. default-role:: py:obj

.. include:: ../NEWS.rst

.. default-role::
