Platform-specific Settings
==========================

.. currentmodule:: sounddevice

.. topic:: Overview

   .. autosummary::
      :nosignatures:

      AlsaSettings
      AsioSettings
      CoreAudioSettings
      WasapiSettings

.. autodata:: DEVICE_FROM_EXTRA_SETTINGS

   Pass this as ``device`` to select a device through ``extra_settings``.
   Device information is unavailable for this value, so channels and sample
   rate must be set explicitly or through defaults, and stream latency must
   be numeric. Format checks do not require latency.

.. autoclass:: AlsaSettings

.. autoclass:: AsioSettings

.. autoclass:: CoreAudioSettings

.. autoclass:: WasapiSettings
