# Copyright (c) 2015-2016 Matthias Geier
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""Play and Record Sound with Python.

http://python-sounddevice.readthedocs.io/

"""
__version__ = '0.3.6'

import atexit as _atexit
from cffi import FFI as _FFI
import os as _os
import platform as _platform
import sys as _sys

_ffi = _FFI()
_ffi.cdef("""
int Pa_GetVersion( void );
const char* Pa_GetVersionText( void );
typedef int PaError;
typedef enum PaErrorCode
{
    paNoError = 0,
    paNotInitialized = -10000,
    paUnanticipatedHostError,
    paInvalidChannelCount,
    paInvalidSampleRate,
    paInvalidDevice,
    paInvalidFlag,
    paSampleFormatNotSupported,
    paBadIODeviceCombination,
    paInsufficientMemory,
    paBufferTooBig,
    paBufferTooSmall,
    paNullCallback,
    paBadStreamPtr,
    paTimedOut,
    paInternalError,
    paDeviceUnavailable,
    paIncompatibleHostApiSpecificStreamInfo,
    paStreamIsStopped,
    paStreamIsNotStopped,
    paInputOverflowed,
    paOutputUnderflowed,
    paHostApiNotFound,
    paInvalidHostApi,
    paCanNotReadFromACallbackStream,
    paCanNotWriteToACallbackStream,
    paCanNotReadFromAnOutputOnlyStream,
    paCanNotWriteToAnInputOnlyStream,
    paIncompatibleStreamHostApi,
    paBadBufferPtr
} PaErrorCode;
const char *Pa_GetErrorText( PaError errorCode );
PaError Pa_Initialize( void );
PaError Pa_Terminate( void );
typedef int PaDeviceIndex;
#define paNoDevice -1
#define paUseHostApiSpecificDeviceSpecification -2
typedef int PaHostApiIndex;
PaHostApiIndex Pa_GetHostApiCount( void );
PaHostApiIndex Pa_GetDefaultHostApi( void );
typedef enum PaHostApiTypeId
{
    paInDevelopment=0,
    paDirectSound=1,
    paMME=2,
    paASIO=3,
    paSoundManager=4,
    paCoreAudio=5,
    paOSS=7,
    paALSA=8,
    paAL=9,
    paBeOS=10,
    paWDMKS=11,
    paJACK=12,
    paWASAPI=13,
    paAudioScienceHPI=14
} PaHostApiTypeId;
typedef struct PaHostApiInfo
{
    int structVersion;
    PaHostApiTypeId type;
    const char *name;
    int deviceCount;
    PaDeviceIndex defaultInputDevice;
    PaDeviceIndex defaultOutputDevice;
} PaHostApiInfo;
const PaHostApiInfo * Pa_GetHostApiInfo( PaHostApiIndex hostApi );
PaHostApiIndex Pa_HostApiTypeIdToHostApiIndex( PaHostApiTypeId type );
PaDeviceIndex Pa_HostApiDeviceIndexToDeviceIndex( PaHostApiIndex hostApi,
        int hostApiDeviceIndex );
typedef struct PaHostErrorInfo{
    PaHostApiTypeId hostApiType;
    long errorCode;
    const char *errorText;
}PaHostErrorInfo;
const PaHostErrorInfo* Pa_GetLastHostErrorInfo( void );
PaDeviceIndex Pa_GetDeviceCount( void );
PaDeviceIndex Pa_GetDefaultInputDevice( void );
PaDeviceIndex Pa_GetDefaultOutputDevice( void );
typedef double PaTime;
typedef unsigned long PaSampleFormat;
#define paFloat32        0x00000001
#define paInt32          0x00000002
#define paInt24          0x00000004
#define paInt16          0x00000008
#define paInt8           0x00000010
#define paUInt8          0x00000020
#define paCustomFormat   0x00010000
#define paNonInterleaved 0x80000000
typedef struct PaDeviceInfo
{
    int structVersion;
    const char *name;
    PaHostApiIndex hostApi;
    int maxInputChannels;
    int maxOutputChannels;
    PaTime defaultLowInputLatency;
    PaTime defaultLowOutputLatency;
    PaTime defaultHighInputLatency;
    PaTime defaultHighOutputLatency;
    double defaultSampleRate;
} PaDeviceInfo;
const PaDeviceInfo* Pa_GetDeviceInfo( PaDeviceIndex device );
typedef struct PaStreamParameters
{
    PaDeviceIndex device;
    int channelCount;
    PaSampleFormat sampleFormat;
    PaTime suggestedLatency;
    void *hostApiSpecificStreamInfo;
} PaStreamParameters;
#define paFormatIsSupported 0
PaError Pa_IsFormatSupported( const PaStreamParameters *inputParameters,
                              const PaStreamParameters *outputParameters,
                              double sampleRate );
typedef void PaStream;
#define paFramesPerBufferUnspecified 0
typedef unsigned long PaStreamFlags;
#define   paNoFlag         0
#define   paClipOff        0x00000001
#define   paDitherOff      0x00000002
#define   paNeverDropInput 0x00000004
#define   paPrimeOutputBuffersUsingStreamCallback 0x00000008
#define   paPlatformSpecificFlags 0xFFFF0000
typedef struct PaStreamCallbackTimeInfo{
    PaTime inputBufferAdcTime;
    PaTime currentTime;
    PaTime outputBufferDacTime;
} PaStreamCallbackTimeInfo;
typedef unsigned long PaStreamCallbackFlags;
#define paInputUnderflow  0x00000001
#define paInputOverflow   0x00000002
#define paOutputUnderflow 0x00000004
#define paOutputOverflow  0x00000008
#define paPrimingOutput   0x00000010
typedef enum PaStreamCallbackResult
{
    paContinue=0,
    paComplete=1,
    paAbort=2
} PaStreamCallbackResult;
typedef int PaStreamCallback(
    const void *input, void *output,
    unsigned long frameCount,
    const PaStreamCallbackTimeInfo* timeInfo,
    PaStreamCallbackFlags statusFlags,
    void *userData );
PaError Pa_OpenStream( PaStream** stream,
                       const PaStreamParameters *inputParameters,
                       const PaStreamParameters *outputParameters,
                       double sampleRate,
                       unsigned long framesPerBuffer,
                       PaStreamFlags streamFlags,
                       PaStreamCallback *streamCallback,
                       void *userData );
PaError Pa_OpenDefaultStream( PaStream** stream,
                              int numInputChannels,
                              int numOutputChannels,
                              PaSampleFormat sampleFormat,
                              double sampleRate,
                              unsigned long framesPerBuffer,
                              PaStreamCallback *streamCallback,
                              void *userData );
PaError Pa_CloseStream( PaStream *stream );
typedef void PaStreamFinishedCallback( void *userData );
PaError Pa_SetStreamFinishedCallback( PaStream *stream,
    PaStreamFinishedCallback* streamFinishedCallback );
PaError Pa_StartStream( PaStream *stream );
PaError Pa_StopStream( PaStream *stream );
PaError Pa_AbortStream( PaStream *stream );
PaError Pa_IsStreamStopped( PaStream *stream );
PaError Pa_IsStreamActive( PaStream *stream );
typedef struct PaStreamInfo
{
    int structVersion;
    PaTime inputLatency;
    PaTime outputLatency;
    double sampleRate;
} PaStreamInfo;
const PaStreamInfo* Pa_GetStreamInfo( PaStream *stream );
PaTime Pa_GetStreamTime( PaStream *stream );
double Pa_GetStreamCpuLoad( PaStream* stream );
PaError Pa_ReadStream( PaStream* stream,
                       void *buffer,
                       unsigned long frames );
PaError Pa_WriteStream( PaStream* stream,
                        const void *buffer,
                        unsigned long frames );
signed long Pa_GetStreamReadAvailable( PaStream* stream );
signed long Pa_GetStreamWriteAvailable( PaStream* stream );
PaHostApiTypeId Pa_GetStreamHostApiType( PaStream* stream );
PaError Pa_GetSampleSize( PaSampleFormat format );
void Pa_Sleep( long msec );

/* pa_win_waveformat.h */

typedef unsigned long PaWinWaveFormatChannelMask;

/* pa_asio.h */

#define paAsioUseChannelSelectors 0x01

typedef struct PaAsioStreamInfo
{
    unsigned long size;
    PaHostApiTypeId hostApiType;
    unsigned long version;
    unsigned long flags;
    int *channelSelectors;
} PaAsioStreamInfo;

/* pa_win_wasapi.h */

typedef enum PaWasapiFlags
{
    paWinWasapiExclusive                = 1,
    paWinWasapiRedirectHostProcessor    = 2,
    paWinWasapiUseChannelMask           = 4,
    paWinWasapiPolling                  = 8,
    paWinWasapiThreadPriority           = 16
} PaWasapiFlags;

typedef void (*PaWasapiHostProcessorCallback) (
    void *inputBuffer,  long inputFrames,
    void *outputBuffer, long outputFrames, void *userData);

typedef enum PaWasapiThreadPriority
{
    eThreadPriorityNone = 0,
    eThreadPriorityAudio,
    eThreadPriorityCapture,
    eThreadPriorityDistribution,
    eThreadPriorityGames,
    eThreadPriorityPlayback,
    eThreadPriorityProAudio,
    eThreadPriorityWindowManager
} PaWasapiThreadPriority;

typedef enum PaWasapiStreamCategory
{
    eAudioCategoryOther           = 0,
    eAudioCategoryCommunications  = 3,
    eAudioCategoryAlerts          = 4,
    eAudioCategorySoundEffects    = 5,
    eAudioCategoryGameEffects     = 6,
    eAudioCategoryGameMedia       = 7,
    eAudioCategoryGameChat        = 8,
    eAudioCategorySpeech          = 9,
    eAudioCategoryMovie           = 10,
    eAudioCategoryMedia           = 11
} PaWasapiStreamCategory;

typedef enum PaWasapiStreamOption
{
    eStreamOptionNone        = 0,
    eStreamOptionRaw         = 1,
    eStreamOptionMatchFormat = 2
} PaWasapiStreamOption;

typedef struct PaWasapiStreamInfo
{
    unsigned long size;
    PaHostApiTypeId hostApiType;
    unsigned long version;
    unsigned long flags;
    PaWinWaveFormatChannelMask channelMask;
    PaWasapiHostProcessorCallback hostProcessorOutput;
    PaWasapiHostProcessorCallback hostProcessorInput;
    PaWasapiThreadPriority threadPriority;
    PaWasapiStreamCategory streamCategory;
    PaWasapiStreamOption streamOption;
} PaWasapiStreamInfo;
""")

try:
    _lib = _ffi.dlopen('portaudio')
except OSError:
    if _platform.system() == 'Darwin':
        _libname = 'libportaudio.dylib'
    elif _platform.system() == 'Windows':
        _libname = 'libportaudio' + _platform.architecture()[0] + '.dll'
    else:
        raise
    _lib = _ffi.dlopen(_os.path.join(
        _os.path.dirname(_os.path.abspath(__file__)),
        '_sounddevice_data',
        _libname
    ))

_sampleformats = {
    'float32': _lib.paFloat32,
    'int32': _lib.paInt32,
    'int24': _lib.paInt24,
    'int16': _lib.paInt16,
    'int8': _lib.paInt8,
    'uint8': _lib.paUInt8,
}

_initialized = 0
_last_callback = None


def play(data, samplerate=None, mapping=None, blocking=False, loop=False,
         **kwargs):
    """Play back a NumPy array containing audio data.

    Parameters
    ----------
    data : array_like
        Audio data to be played back.  The columns of a two-dimensional
        array are interpreted as channels, one-dimensional arrays are
        treated as mono data.
        The data types *float64*, *float32*, *int32*, *int16*, *int8*
        and *uint8* can be used.
        *float64* data is converted to *float32* before passing it to
        PortAudio, because it's not supported natively.
    mapping : array_like, optional
        List of channel numbers (starting with 1) where the columns of
        *data* shall be played back on.  Must have the same length as
        number of channels in *data* (except if *data* is mono).
        Each channel may only appear once in *mapping*.
    blocking : bool, optional
        If ``False`` (the default), return immediately (but playback
        continues in the background), if ``True``, wait until playback
        is finished.  A non-blocking invocation can be stopped with
        `stop()` or turned into a blocking one with `wait()`.
    loop : bool, optional
        Play *data* in a loop.

    Other Parameters
    ----------------
    samplerate, **kwargs
        All parameters of `OutputStream` -- except *channels*, *dtype*,
        *callback* and *finished_callback* -- can be used.

    See Also
    --------
    rec, playrec

    """
    ctx = _CallbackContext(loop=loop)
    ctx.frames = ctx.check_data(data, mapping, kwargs.get('device'))

    def callback(outdata, frames, time, status):
        assert len(outdata) == frames
        ctx.callback_enter(status, outdata)
        ctx.write_outdata(outdata)
        ctx.callback_exit()

    ctx.start_stream(OutputStream, samplerate, ctx.output_channels,
                     ctx.output_dtype, callback, blocking,
                     prime_output_buffers_using_stream_callback=False,
                     **kwargs)


def rec(frames=None, samplerate=None, channels=None, dtype=None,
        out=None, mapping=None, blocking=False, **kwargs):
    """Record audio data into a NumPy array.

    Parameters
    ----------
    frames : int, sometimes optional
        Number of frames to record.  Not needed if *out* is given.
    channels : int, optional
        Number of channels to record.  Not needed if *mapping* or *out*
        is given.  The default value can be changed with
        `default.channels`.
    dtype : str or numpy.dtype, optional
        Data type of the recording.  Not needed if *out* is given.
        The data types *float64*, *float32*, *int32*, *int16*, *int8*
        and *uint8* can be used.  For ``dtype='float64'``, audio data is
        recorded in *float32* format and converted afterwards, because
        it's not natively supported by PortAudio.  The default value can
        be changed with `default.dtype`.
    mapping : array_like, optional
        List of channel numbers (starting with 1) to record.
        If *mapping* is given, *channels* is silently ignored.
    blocking : bool, optional
        If ``False`` (the default), return immediately (but recording
        continues in the background), if ``True``, wait until recording
        is finished.
        A non-blocking invocation can be stopped with `stop()` or turned
        into a blocking one with `wait()`.

    Returns
    -------
    numpy.ndarray or type(out)
        The recorded data.

        .. note:: By default (``blocking=False``), an array of data is
           returned which is still being written to while recording.
           The returned data is only valid once recording has stopped.
           Use `wait()` to make sure the recording is finished.

    Other Parameters
    ----------------
    out : numpy.ndarray or subclass, optional
        If *out* is specified, the recorded data is written into the
        given array instead of creating a new array.
        In this case, the arguments *frames*, *channels* and *dtype* are
        silently ignored!
        If *mapping* is given, its length must match the number of
        channels in *out*.
    samplerate, **kwargs
        All parameters of `InputStream` -- except *callback* and
        *finished_callback* -- can be used.

    See Also
    --------
    play, playrec

    """
    ctx = _CallbackContext()
    ctx.frames = ctx.check_out(out, frames, channels, dtype, mapping)

    def callback(indata, frames, time, status):
        assert len(indata) == frames
        ctx.callback_enter(status, indata)
        ctx.read_indata(indata)
        ctx.callback_exit()

    ctx.start_stream(InputStream, samplerate, ctx.input_channels,
                     ctx.input_dtype, callback, blocking, **kwargs)
    return ctx.out


def playrec(data, samplerate=None, channels=None, dtype=None,
            out=None, input_mapping=None, output_mapping=None, blocking=False,
            **kwargs):
    """Simultaneous playback and recording of NumPy arrays.

    Parameters
    ----------
    data : array_like
        Audio data to be played back.  See `play()`.
    channels : int, sometimes optional
        Number of input channels, see `rec()`.
        The number of output channels is obtained from *data.shape*.
    dtype : str or numpy.dtype, optional
        Input data type, see `rec()`.
        If *dtype* is not specified, it is taken from *data.dtype*
        (i.e. `default.dtype` is ignored).
        The output data type is obtained from *data.dtype* anyway.
    input_mapping, output_mapping : array_like, optional
        See the parameter *mapping* of `rec()` and `play()`,
        respectively.
    blocking : bool, optional
        If ``False`` (the default), return immediately (but continue
        playback/recording in the background), if ``True``, wait until
        playback/recording is finished.
        A non-blocking invocation can be stopped with `stop()` or turned
        into a blocking one with `wait()`.

    Returns
    -------
    numpy.ndarray or type(out)
        The recorded data.  See `rec()`.

    Other Parameters
    ----------------
    out : numpy.ndarray or subclass, optional
        See `rec()`.
    samplerate, **kwargs
        All parameters of `Stream` -- except *channels*, *dtype*,
        *callback* and *finished_callback* -- can be used.

    See Also
    --------
    play, rec

    """
    ctx = _CallbackContext()
    output_frames = ctx.check_data(data, output_mapping, kwargs.get('device'))
    if dtype is None:
        dtype = ctx.data.dtype  # ignore module defaults
    input_frames = ctx.check_out(out, output_frames, channels, dtype,
                                 input_mapping)
    if input_frames != output_frames:
        raise PortAudioError('len(data) != len(out)')
    ctx.frames = input_frames

    def callback(indata, outdata, frames, time, status):
        assert len(indata) == len(outdata) == frames
        ctx.callback_enter(status, indata)
        ctx.read_indata(indata)
        ctx.write_outdata(outdata)
        ctx.callback_exit()

    ctx.start_stream(Stream, samplerate,
                     (ctx.input_channels, ctx.output_channels),
                     (ctx.input_dtype, ctx.output_dtype),
                     callback, blocking,
                     prime_output_buffers_using_stream_callback=False,
                     **kwargs)
    return ctx.out


def wait():
    """Wait for `play()`/`rec()`/`playrec()` to be finished.

    Playback/recording can be stopped with a `KeyboardInterrupt`.

    Returns
    -------
    CallbackFlags or None
        If at least one buffer over-/underrun happened during the last
        playback/recording, a `CallbackFlags` object is returned.

    See Also
    --------
    get_status

    """
    if _last_callback:
        return _last_callback.wait()


def stop(ignore_errors=True):
    """Stop playback/recording.

    This only stops `play()`, `rec()` and `playrec()`, but has no
    influence on streams created with `Stream`, `InputStream`,
    `OutputStream`, `RawStream`, `RawInputStream`, `RawOutputStream`.

    """
    if _last_callback:
        _last_callback.stream.close(ignore_errors)


def get_status():
    """Get info about over-/underflows in `play()`/`rec()`/`playrec()`.

    Returns
    -------
    CallbackFlags
        A `CallbackFlags` object that holds information about the last
        invocation of `play()`, `rec()` or `playrec()`.

    See Also
    --------
    wait

    """
    if _last_callback:
        return _last_callback.status
    else:
        raise RuntimeError('play()/rec()/playrec() was not called yet')


def query_devices(device=None, kind=None):
    """Return information about available devices.

    Information and capabilities of PortAudio devices.
    Devices may support input, output or both input and output.

    To find the default input/output device(s), use `default.device`.

    Parameters
    ----------
    device : int or str, optional
        Numeric device ID or device name substring(s).
        If specified, information about only the given *device* is
        returned in a single dictionary.
    kind : {'input', 'output'}, optional
        If *device* is not specified and *kind* is ``'input'`` or
        ``'output'``, a single dictionary is returned with information
        about the default input or output device, respectively.

    Returns
    -------
    dict or DeviceList
        A dictionary with information about the given *device* or -- if
        no *device* was specified -- a `DeviceList` containing one
        dictionary for each available device.
        The dictionaries have the following keys:

        ``'name'``
            The name of the device.
        ``'hostapi'``
            The ID of the corresponding host API.  Use
            `query_hostapis()` to get information about a host API.
        ``'max_input_channels'``, ``'max_output_channels'``
            The maximum number of input/output channels supported by the
            device.  See `default.channels`.
        ``'default_low_input_latency'``, ``'default_low_output_latency'``
            Default latency values for interactive performance.
            This is used if `default.latency` (or the *latency* argument
            of `playrec()`, `Stream` etc.) is set to ``'low'``.
        ``'default_high_input_latency'``, ``'default_high_output_latency'``
            Default latency values for robust non-interactive
            applications (e.g. playing sound files).
            This is used if `default.latency` (or the *latency* argument
            of `playrec()`, `Stream` etc.) is set to ``'high'``.
        ``'default_samplerate'``
            The default sampling frequency of the device.
            This is used if `default.samplerate` is not set.

    Notes
    -----
    The list of devices can also be displayed in a terminal:

    .. code-block:: sh

        python3 -m sounddevice

    Examples
    --------
    The returned `DeviceList` can be indexed and iterated over like any
    sequence type (yielding the abovementioned dictionaries), but it
    also has a special string representation which is shown when used in
    an interactive Python session.

    Each available device is listed on one line together with the
    corresponding device ID, which can be assigned to `default.device`
    or used as *device* argument in `play()`, `Stream` etc.

    The first character of a line is ``>`` for the default input device,
    ``<`` for the default output device and ``*`` for the default
    input/output device.  After the device ID and the device name, the
    corresponding host API name is displayed.  In the end of each line,
    the maximum number of input and output channels is shown.

    On a GNU/Linux computer it might look somewhat like this:

    >>> import sounddevice as sd
    >>> sd.query_devices()
       0 HDA Intel: ALC662 rev1 Analog (hw:0,0), ALSA (2 in, 2 out)
       1 HDA Intel: ALC662 rev1 Digital (hw:0,1), ALSA (0 in, 2 out)
       2 HDA Intel: HDMI 0 (hw:0,3), ALSA (0 in, 8 out)
       3 sysdefault, ALSA (128 in, 128 out)
       4 front, ALSA (0 in, 2 out)
       5 surround40, ALSA (0 in, 2 out)
       6 surround51, ALSA (0 in, 2 out)
       7 surround71, ALSA (0 in, 2 out)
       8 iec958, ALSA (0 in, 2 out)
       9 spdif, ALSA (0 in, 2 out)
      10 hdmi, ALSA (0 in, 8 out)
    * 11 default, ALSA (128 in, 128 out)
      12 dmix, ALSA (0 in, 2 out)
      13 /dev/dsp, OSS (16 in, 16 out)

    Note that ALSA provides access to some "real" and some "virtual"
    devices.  The latter sometimes have a ridiculously high number of
    (virtual) inputs and outputs.

    On Mac OS X, you might get something similar to this:

    >>> sd.query_devices()
      0 Built-in Line Input, Core Audio (2 in, 0 out)
    > 1 Built-in Digital Input, Core Audio (2 in, 0 out)
    < 2 Built-in Output, Core Audio (0 in, 2 out)
      3 Built-in Line Output, Core Audio (0 in, 2 out)
      4 Built-in Digital Output, Core Audio (0 in, 2 out)

    """
    if kind not in ('input', 'output', None):
        raise ValueError('Invalid kind: {0!r}'.format(kind))
    if device is None and kind is None:
        return DeviceList(query_devices(i)
                          for i in range(_check(_lib.Pa_GetDeviceCount())))
    device = _get_device_id(device, kind, raise_on_error=True)
    info = _lib.Pa_GetDeviceInfo(device)
    if not info:
        raise PortAudioError('Error querying device {0}'.format(device))
    assert info.structVersion == 2
    device_dict = {
        'name': _ffi.string(info.name).decode('mbcs' if info.hostApi in (
            _lib.Pa_HostApiTypeIdToHostApiIndex(_lib.paDirectSound),
            _lib.Pa_HostApiTypeIdToHostApiIndex(_lib.paMME)) else 'utf-8'),
        'hostapi': info.hostApi,
        'max_input_channels': info.maxInputChannels,
        'max_output_channels': info.maxOutputChannels,
        'default_low_input_latency': info.defaultLowInputLatency,
        'default_low_output_latency': info.defaultLowOutputLatency,
        'default_high_input_latency': info.defaultHighInputLatency,
        'default_high_output_latency': info.defaultHighOutputLatency,
        'default_samplerate': info.defaultSampleRate,
    }
    if kind and device_dict['max_' + kind + '_channels'] < 1:
        raise ValueError(
            'Not an {0} device: {1!r}'.format(kind, device_dict['name']))
    return device_dict


def query_hostapis(index=None):
    """Return information about available host APIs.

    Parameters
    ----------
    index : int, optional
        If specified, information about only the given host API *index*
        is returned in a single dictionary.

    Returns
    -------
    dict or tuple of dict
        A dictionary with information about the given host API *index*
        or -- if no *index* was specified -- a tuple containing one
        dictionary for each available host API.
        The dictionaries have the following keys:

        ``'name'``
            The name of the host API.
        ``'devices'``
            A list of device IDs belonging to the host API.
            Use `query_devices()` to get information about a device.
        ``'default_input_device'``, ``'default_output_device'``
            The device ID of the default input/output device of the host
            API.  If no default input/output device exists for the given
            host API, this is -1.

            .. note:: The overall default device(s) -- which can be
                overwritten by assigning to `default.device` -- take(s)
                precedence over `default.hostapi` and the information in
                the abovementioned dictionaries.

    See Also
    --------
    query_devices

    """
    if index is None:
        return tuple(query_hostapis(i)
                     for i in range(_check(_lib.Pa_GetHostApiCount())))
    info = _lib.Pa_GetHostApiInfo(index)
    if not info:
        raise PortAudioError('Error querying host API {0}'.format(index))
    assert info.structVersion == 1
    return {
        'name': _ffi.string(info.name).decode(),
        'devices': [_lib.Pa_HostApiDeviceIndexToDeviceIndex(index, i)
                    for i in range(info.deviceCount)],
        'default_input_device': info.defaultInputDevice,
        'default_output_device': info.defaultOutputDevice,
    }


def check_input_settings(device=None, channels=None, dtype=None,
                         extra_settings=None, samplerate=None):
    """Check if given input device settings are supported.

    All parameters are optional, `default` settings are used for any
    unspecified parameters.  If the settings are supported, the function
    does nothing; if not, an exception is raised.

    Parameters
    ----------
    device : int or str, optional
        Device ID or device name substring, see `default.device`.
    channels : int, optional
        Number of input channels, see `default.channels`.
    dtype : str or numpy.dtype, optional
        Data type for input samples, see `default.dtype`.
    extra_settings : settings object, optional
        This can be used for host-API-specific input settings.
        See `default.extra_settings`.
    samplerate : float, optional
        Sampling frequency, see `default.samplerate`.

    """
    parameters, dtype, samplesize, samplerate = _get_stream_parameters(
        'input', device=device, channels=channels, dtype=dtype, latency=None,
        extra_settings=extra_settings, samplerate=samplerate)
    _check(_lib.Pa_IsFormatSupported(parameters, _ffi.NULL, samplerate))


def check_output_settings(device=None, channels=None, dtype=None,
                          extra_settings=None, samplerate=None):
    """Check if given output device settings are supported.

    Same as `check_input_settings()`, just for output device
    settings.

    """
    parameters, dtype, samplesize, samplerate = _get_stream_parameters(
        'output', device=device, channels=channels, dtype=dtype, latency=None,
        extra_settings=extra_settings, samplerate=samplerate)
    _check(_lib.Pa_IsFormatSupported(_ffi.NULL, parameters, samplerate))


def sleep(msec):
    """Put the caller to sleep for at least *msec* milliseconds.

    The function may sleep longer than requested so don't rely on this
    for accurate musical timing.

    """
    _lib.Pa_Sleep(msec)


def get_portaudio_version():
    """Get version information for the PortAudio library.

    Returns the release number and a textual description of the current
    PortAudio build, e.g. ::

        (1899, 'PortAudio V19-devel (built Feb 15 2014 23:28:00)')

    """
    return _lib.Pa_GetVersion(), _ffi.string(_lib.Pa_GetVersionText()).decode()


class _StreamBase(object):
    """Base class for Raw{Input,Output}Stream."""

    def __init__(self, kind, samplerate, blocksize, device, channels, dtype,
                 latency, extra_settings, callback_wrapper, finished_callback,
                 clip_off, dither_off, never_drop_input,
                 prime_output_buffers_using_stream_callback):
        if blocksize is None:
            blocksize = default.blocksize
        if clip_off is None:
            clip_off = default.clip_off
        if dither_off is None:
            dither_off = default.dither_off
        if never_drop_input is None:
            never_drop_input = default.never_drop_input
        if prime_output_buffers_using_stream_callback is None:
            prime_output_buffers_using_stream_callback = \
                default.prime_output_buffers_using_stream_callback

        stream_flags = _lib.paNoFlag
        if clip_off:
            stream_flags |= _lib.paClipOff
        if dither_off:
            stream_flags |= _lib.paDitherOff
        if never_drop_input:
            stream_flags |= _lib.paNeverDropInput
        if prime_output_buffers_using_stream_callback:
            stream_flags |= _lib.paPrimeOutputBuffersUsingStreamCallback

        if kind == 'duplex':
            idevice, odevice = _split(device)
            ichannels, ochannels = _split(channels)
            idtype, odtype = _split(dtype)
            ilatency, olatency = _split(latency)
            iextra, oextra = _split(extra_settings)
            iparameters, idtype, isize, isamplerate = _get_stream_parameters(
                'input', idevice, ichannels, idtype, ilatency, iextra,
                samplerate)
            oparameters, odtype, osize, osamplerate = _get_stream_parameters(
                'output', odevice, ochannels, odtype, olatency, oextra,
                samplerate)
            self._dtype = idtype, odtype
            self._device = iparameters.device, oparameters.device
            self._channels = iparameters.channelCount, oparameters.channelCount
            self._samplesize = isize, osize
            if isamplerate != osamplerate:
                raise PortAudioError(
                    'Input and output device must have the same samplerate')
            else:
                samplerate = isamplerate
        else:
            parameters, self._dtype, self._samplesize, samplerate = \
                _get_stream_parameters(kind, device, channels, dtype, latency,
                                       extra_settings, samplerate)
            self._device = parameters.device
            self._channels = parameters.channelCount

            if kind == 'input':
                iparameters = parameters
                oparameters = _ffi.NULL
            elif kind == 'output':
                iparameters = _ffi.NULL
                oparameters = parameters

        if callback_wrapper:
            self._callback = _ffi.callback(
                'PaStreamCallback', callback_wrapper, error=_lib.paAbort)
        else:
            self._callback = _ffi.NULL

        self._ptr = _ffi.new('PaStream**')
        _check(_lib.Pa_OpenStream(self._ptr, iparameters, oparameters,
                                  samplerate, blocksize, stream_flags,
                                  self._callback, _ffi.NULL),
               'Error opening {0}'.format(self.__class__.__name__))

        # dereference PaStream** --> PaStream*
        self._ptr = self._ptr[0]

        self._blocksize = blocksize
        info = _lib.Pa_GetStreamInfo(self._ptr)
        if not info:
            raise PortAudioError('Could not obtain stream info')
        # TODO: assert info.structVersion == 1
        self._samplerate = info.sampleRate
        if not oparameters:
            self._latency = info.inputLatency
        elif not iparameters:
            self._latency = info.outputLatency
        else:
            self._latency = info.inputLatency, info.outputLatency

        if finished_callback:

            def finished_callback_wrapper(_):
                return finished_callback()

            self._finished_callback = _ffi.callback(
                'PaStreamFinishedCallback', finished_callback_wrapper)
            _check(_lib.Pa_SetStreamFinishedCallback(self._ptr,
                                                     self._finished_callback))

    # Avoid confusion if something goes wrong before assigning self._ptr:
    _ptr = _ffi.NULL

    @property
    def samplerate(self):
        """The sampling frequency in Hertz (= frames per second).

        In cases where the hardware sampling frequency is inaccurate and
        PortAudio is aware of it, the value of this field may be
        different from the *samplerate* parameter passed to `Stream()`.
        If information about the actual hardware sampling frequency is
        not available, this field will have the same value as the
        *samplerate* parameter passed to `Stream()`.

        """
        return self._samplerate

    @property
    def blocksize(self):
        """Number of frames per block.

        The special value 0 means that the blocksize can change between
        blocks.  See the *blocksize* argument of `Stream`.

        """
        return self._blocksize

    @property
    def device(self):
        """IDs of the input/output device."""
        return self._device

    @property
    def channels(self):
        """The number of input/output channels."""
        return self._channels

    @property
    def dtype(self):
        """Data type of the audio samples.

        See Also
        --------
        default.dtype, samplesize

        """
        return self._dtype

    @property
    def samplesize(self):
        """The size in bytes of a single sample.

        See Also
        --------
        dtype

        """
        return self._samplesize

    @property
    def latency(self):
        """The input/output latency of the stream in seconds.

        This value provides the most accurate estimate of input/output
        latency available to the implementation.
        It may differ significantly from the *latency* value(s) passed
        to `Stream()`.

        """
        return self._latency

    @property
    def active(self):
        """``True`` when the stream is active, ``False`` otherwise.

        A stream is active after a successful call to `start()`, until
        it becomes inactive either as a result of a call to `stop()` or
        `abort()`, or as a result of an exception raised in the stream
        callback.  In the latter case, the stream is considered inactive
        after the last buffer has finished playing.

        See Also
        --------
        stopped

        """
        return _check(_lib.Pa_IsStreamActive(self._ptr)) == 1

    @property
    def stopped(self):
        """``True`` when the stream is stopped, ``False`` otherwise.

        A stream is considered to be stopped prior to a successful call
        to `start()` and after a successful call to `stop()` or
        `abort()`.  If a stream callback is cancelled (by raising an
        exception) the stream is *not* considered to be stopped.

        See Also
        --------
        active

        """
        return _check(_lib.Pa_IsStreamStopped(self._ptr)) == 1

    @property
    def time(self):
        """The current stream time in seconds.

        This is according to the same clock used to generate the
        timestamps passed with the *time* argument to the stream
        callback (see the *callback* argument of `Stream`).
        The time values are monotonically increasing and have
        unspecified origin.

        This provides valid time values for the entire life of the
        stream, from when the stream is opened until it is closed.
        Starting and stopping the stream does not affect the passage of
        time as provided here.

        This time may be used for synchronizing other events to the
        audio stream, for example synchronizing audio to MIDI.

        """
        time = _lib.Pa_GetStreamTime(self._ptr)
        if not time:
            raise PortAudioError('Error getting stream time')
        return time

    @property
    def cpu_load(self):
        """CPU usage information for the stream.

        The "CPU Load" is a fraction of total CPU time consumed by a
        callback stream's audio processing routines including, but not
        limited to the client supplied stream callback. This function
        does not work with blocking read/write streams.

        This may be used in the stream callback function or in the
        application.
        It provides a floating point value, typically between 0.0 and
        1.0, where 1.0 indicates that the stream callback is consuming
        the maximum number of CPU cycles possible to maintain real-time
        operation.  A value of 0.5 would imply that PortAudio and the
        stream callback was consuming roughly 50% of the available CPU
        time.  The value may exceed 1.0.  A value of 0.0 will always be
        returned for a blocking read/write stream, or if an error
        occurs.

        """
        return _lib.Pa_GetStreamCpuLoad(self._ptr)

    def __del__(self):
        """Close stream at garbage collection."""
        self.close()

    def __enter__(self):
        """Start  the stream in the beginning of a "with" statement."""
        self.start()
        return self

    def __exit__(self, *args):
        """Stop and close the stream when exiting a "with" statement."""
        self.stop()
        self.close()

    def start(self):
        """Commence audio processing.

        See Also
        --------
        stop, abort

        """
        err = _lib.Pa_StartStream(self._ptr)
        if err != _lib.paStreamIsNotStopped:
            _check(err, 'Error starting stream')

    def stop(self):
        """Terminate audio processing.

        This waits until all pending audio buffers have been played
        before it returns.

        See Also
        --------
        start, abort

        """
        err = _lib.Pa_StopStream(self._ptr)
        if err != _lib.paStreamIsStopped:
            _check(err, 'Error stopping stream')

    def abort(self):
        """Terminate audio processing immediately.

        This does not wait for pending buffers to complete.

        See Also
        --------
        start, stop

        """
        err = _lib.Pa_AbortStream(self._ptr)
        if err != _lib.paStreamIsStopped:
            _check(err, 'Error aborting stream')

    def close(self, ignore_errors=True):
        """Close the stream.

        If the audio stream is active any pending buffers are discarded
        as if `abort()` had been called.

        """
        err = _lib.Pa_CloseStream(self._ptr)
        if not ignore_errors:
            _check(err, 'Error closing stream')


class RawInputStream(_StreamBase):
    """Raw stream for recording only.  See __init__() and RawStream."""

    def __init__(self, samplerate=None, blocksize=None,
                 device=None, channels=None, dtype=None, latency=None,
                 extra_settings=None, callback=None, finished_callback=None,
                 clip_off=None, dither_off=None, never_drop_input=None,
                 prime_output_buffers_using_stream_callback=None):
        """Open a "raw" input stream.

        This is the same as `InputStream`, except that the *callback*
        function and :meth:`~RawStream.read` work on plain Python buffer
        objects instead of on NumPy arrays.
        NumPy is not necessary to use this.

        Parameters
        ----------
        dtype : str
            See `RawStream`.
        callback : callable
            User-supplied function to consume audio data in response to
            requests from an active stream.
            The callback must have this signature::

                callback(indata: buffer, frames: int,
                         time: CData, status: CallbackFlags) -> None

            The arguments are the same as in the *callback* parameter of
            `RawStream`, except that *outdata* is missing.

        See Also
        --------
        RawStream, Stream

        """

        def callback_wrapper(iptr, optr, frames, time, status, _):
            data = _buffer(iptr, frames, self._channels, self._samplesize)
            return _wrap_callback(callback, data, frames, time, status)

        _StreamBase.__init__(
            self, 'input', samplerate, blocksize, device, channels, dtype,
            latency, extra_settings, callback and callback_wrapper,
            finished_callback, clip_off, dither_off, never_drop_input,
            prime_output_buffers_using_stream_callback)

    @property
    def read_available(self):
        """The number of frames that can be read without waiting.

        Returns a value representing the maximum number of frames that
        can be read from the stream without blocking or busy waiting.

        """
        return _check(_lib.Pa_GetStreamReadAvailable(self._ptr))

    def read(self, frames):
        """Read samples from the stream into a buffer.

        This is the same as `Stream.read()`, except that it returns
        a plain Python buffer object instead of a NumPy array.
        NumPy is not necessary to use this.

        Parameters
        ----------
        frames : int
            The number of frames to be read.  See `Stream.read()`.

        Returns
        -------
        data : buffer
            A buffer of interleaved samples. The buffer contains
            samples in the format specified by the *dtype* parameter
            used to open the stream, and the number of channels
            specified by *channels*.
            See also `samplesize`.
        overflowed : bool
            See `Stream.read()`.

        """
        channels, _ = _split(self._channels)
        samplesize, _ = _split(self._samplesize)
        data = _ffi.new('signed char[]', channels * samplesize * frames)
        err = _lib.Pa_ReadStream(self._ptr, data, frames)
        if err == _lib.paInputOverflowed:
            overflowed = True
        else:
            _check(err)
            overflowed = False
        return _ffi.buffer(data), overflowed


class RawOutputStream(_StreamBase):
    """Raw stream for playback only.  See __init__() and RawStream."""

    def __init__(self, samplerate=None, blocksize=None,
                 device=None, channels=None, dtype=None, latency=None,
                 extra_settings=None, callback=None, finished_callback=None,
                 clip_off=None, dither_off=None, never_drop_input=None,
                 prime_output_buffers_using_stream_callback=None):
        """Open a "raw" output stream.

        This is the same as `OutputStream`, except that the *callback*
        function and :meth:`~RawStream.write` work on plain Python
        buffer objects instead of on NumPy arrays.
        NumPy is not necessary to use this.

        Parameters
        ----------
        dtype : str
            See `RawStream`.
        callback : callable
            User-supplied function to generate audio data in response to
            requests from an active stream.
            The callback must have this signature::

                callback(outdata: buffer, frames: int,
                         time: CData, status: CallbackFlags) -> None

            The arguments are the same as in the *callback* parameter of
            `RawStream`, except that *indata* is missing.

        See Also
        --------
        RawStream, Stream

        """

        def callback_wrapper(iptr, optr, frames, time, status, _):
            data = _buffer(optr, frames, self._channels, self._samplesize)
            return _wrap_callback(callback, data, frames, time, status)

        _StreamBase.__init__(
            self, 'output', samplerate, blocksize, device, channels, dtype,
            latency, extra_settings, callback and callback_wrapper,
            finished_callback, clip_off, dither_off, never_drop_input,
            prime_output_buffers_using_stream_callback)

    @property
    def write_available(self):
        """The number of frames that can be written without waiting.

        Returns a value representing the maximum number of frames that
        can be written to the stream without blocking or busy waiting.

        """
        return _check(_lib.Pa_GetStreamWriteAvailable(self._ptr))

    def write(self, data):
        """Write samples to the stream.

        This is the same as `Stream.write()`, except that it expects
        a plain Python buffer object instead of a NumPy array.
        NumPy is not necessary to use this.

        Parameters
        ----------
        data : buffer or bytes or iterable of int
            A buffer of interleaved samples.  The buffer contains
            samples in the format specified by the *dtype* argument used
            to open the stream, and the number of channels specified by
            *channels*.  The length of the buffer is not constrained to
            a specific range, however high performance applications will
            want to match this parameter to the *blocksize* parameter
            used when opening the stream.  See also `samplesize`.

        Returns
        -------
        underflowed : bool
            See `Stream.write()`.

        """
        try:
            data = _ffi.from_buffer(data)
        except AttributeError:
            pass  # from_buffer() not supported
        except TypeError:
            pass  # input is not a buffer
        _, samplesize = _split(self._samplesize)
        _, channels = _split(self._channels)
        samples, remainder = divmod(len(data), samplesize)
        if remainder:
            raise ValueError('len(data) not divisible by samplesize')
        frames, remainder = divmod(samples, channels)
        if remainder:
            raise ValueError('Number of samples not divisible by channels')
        err = _lib.Pa_WriteStream(self._ptr, data, frames)
        if err == _lib.paOutputUnderflowed:
            underflowed = True
        else:
            _check(err)
            underflowed = False
        return underflowed


class RawStream(RawInputStream, RawOutputStream):
    """Raw stream for playback and recording.  See __init__()."""

    def __init__(self, samplerate=None, blocksize=None,
                 device=None, channels=None, dtype=None, latency=None,
                 extra_settings=None, callback=None, finished_callback=None,
                 clip_off=None, dither_off=None, never_drop_input=None,
                 prime_output_buffers_using_stream_callback=None):
        """Open a "raw" input/output stream.

        This is the same as `Stream`, except that the *callback*
        function and `read()`/`write()` work on plain Python buffer
        objects instead of on NumPy arrays.
        NumPy is not necessary to use this.

        To open "raw" input-only or output-only stream use
        `RawInputStream` or `RawOutputStream`, respectively.
        If you want to handle audio data as NumPy arrays instead of
        buffer objects, use `Stream`, `InputStream` or `OutputStream`.

        Parameters
        ----------
        dtype : str or pair of str
            The sample format of the buffers provided to the stream
            callback, `read()` or `write()`.
            In addition to the formats supported by `Stream`
            (``'float32'``, ``'int32'``, ``'int16'``, ``'int8'``,
            ``'uint8'``), this also supports ``'int24'``, i.e.
            packed 24 bit format.
            The default value can be changed with `default.dtype`.
            See also `samplesize`.
        callback : callable
            User-supplied function to consume, process or generate audio
            data in response to requests from an active stream.
            The callback must have this signature::

                callback(indata: buffer, outdata: buffer, frames: int,
                         time: CData, status: CallbackFlags) -> None

            The arguments are the same as in the *callback* parameter of
            `Stream`, except that *indata* and *outdata* are plain
            Python buffer objects instead of NumPy arrays.

        See Also
        --------
        RawInputStream, RawOutputStream, Stream

        """

        def callback_wrapper(iptr, optr, frames, time, status, _):
            ichannels, ochannels = self._channels
            isize, osize = self._samplesize
            idata = _buffer(iptr, frames, ichannels, isize)
            odata = _buffer(optr, frames, ochannels, osize)
            return _wrap_callback(callback, idata, odata, frames, time, status)

        _StreamBase.__init__(
            self, 'duplex', samplerate, blocksize, device, channels, dtype,
            latency, extra_settings, callback and callback_wrapper,
            finished_callback, clip_off, dither_off, never_drop_input,
            prime_output_buffers_using_stream_callback)


class InputStream(RawInputStream):
    """Stream for input only.  See __init__() and Stream."""

    def __init__(self, samplerate=None, blocksize=None,
                 device=None, channels=None, dtype=None, latency=None,
                 extra_settings=None, callback=None, finished_callback=None,
                 clip_off=None, dither_off=None, never_drop_input=None,
                 prime_output_buffers_using_stream_callback=None):
        """Open an input stream.

        This has the same methods and attributes as `Stream`, except
        :meth:`~Stream.write` and `write_available`.
        Furthermore, the stream callback is expected to have a different
        signature (see below).

        Parameters
        ----------
        callback : callable
            User-supplied function to consume audio in response to
            requests from an active stream.
            The callback must have this signature::

                callback(indata: numpy.ndarray, frames: int,
                         time: CData, status: CallbackFlags) -> None

            The arguments are the same as in the *callback* parameter of
            `Stream`, except that *outdata* is missing.

        See Also
        --------
        Stream, RawInputStream

        """

        def callback_wrapper(iptr, optr, frames, time, status, _):
            buffer = _buffer(iptr, frames, self._channels, self._samplesize)
            data = _array(buffer, self._channels, self._dtype)
            return _wrap_callback(callback, data, frames, time, status)

        _StreamBase.__init__(
            self, 'input', samplerate, blocksize, device, channels, dtype,
            latency, extra_settings, callback and callback_wrapper,
            finished_callback, clip_off, dither_off, never_drop_input,
            prime_output_buffers_using_stream_callback)

    def read(self, frames):
        """Read samples from the stream into a NumPy array.

        The function doesn't return until all requested *frames* have
        been read -- this may involve waiting for the operating system
        to supply the data (except if no more than `read_available`
        frames were requested).

        This is the same as `RawStream.read()`, except that it
        returns a NumPy array instead of a plain Python buffer object.

        Parameters
        ----------
        frames : int
            The number of frames to be read.  This parameter is not
            constrained to a specific range, however high performance
            applications will want to match this parameter to the
            *blocksize* parameter used when opening the stream.

        Returns
        -------
        data : numpy.ndarray
            A two-dimensional `numpy.ndarray` with one column per
            channel (i.e.  with a shape of ``(frames, channels)``) and
            with a data type specified by `dtype`.
        overflowed : bool
            ``True`` if input data was discarded by PortAudio after the
            previous call and before this call.

        """
        dtype, _ = _split(self._dtype)
        channels, _ = _split(self._channels)
        data, overflowed = RawInputStream.read(self, frames)
        data = _array(data, channels, dtype)
        return data, overflowed


class OutputStream(RawOutputStream):
    """Stream for output only.  See __init__() and Stream."""

    def __init__(self, samplerate=None, blocksize=None,
                 device=None, channels=None, dtype=None, latency=None,
                 extra_settings=None, callback=None, finished_callback=None,
                 clip_off=None, dither_off=None, never_drop_input=None,
                 prime_output_buffers_using_stream_callback=None):
        """Open an output stream.

        This has the same methods and attributes as `Stream`, except
        :meth:`~Stream.read` and `read_available`.
        Furthermore, the stream callback is expected to have a different
        signature (see below).

        Parameters
        ----------
        callback : callable
            User-supplied function to generate audio data in response to
            requests from an active stream.
            The callback must have this signature::

                callback(outdata: numpy.ndarray, frames: int,
                         time: CData, status: CallbackFlags) -> None

            The arguments are the same as in the *callback* parameter of
            `Stream`, except that *indata* is missing.

        See Also
        --------
        Stream, RawOutputStream

        """

        def callback_wrapper(iptr, optr, frames, time, status, _):
            buffer = _buffer(optr, frames, self._channels, self._samplesize)
            data = _array(buffer, self._channels, self._dtype)
            return _wrap_callback(callback, data, frames, time, status)

        _StreamBase.__init__(
            self, 'output', samplerate, blocksize, device, channels, dtype,
            latency, extra_settings, callback and callback_wrapper,
            finished_callback, clip_off, dither_off, never_drop_input,
            prime_output_buffers_using_stream_callback)

    def write(self, data):
        """Write samples to the stream.

        This function doesn't return until the entire buffer has been
        consumed -- this may involve waiting for the operating system to
        consume the data (except if *data* contains no more than
        `write_available` frames).

        This is the same as `RawStream.write()`, except that it
        expects a NumPy array instead of a plain Python buffer object.

        Parameters
        ----------
        data : array_like
            A two-dimensional array-like object with one column per
            channel (i.e.  with a shape of ``(frames, channels)``) and
            with a data type specified by `dtype`.  A one-dimensional
            array can be used for mono data.  The array layout must be
            C-contiguous (see :func:`numpy.ascontiguousarray`).

            The length of the buffer is not constrained to a specific
            range, however high performance applications will want to
            match this parameter to the *blocksize* parameter used when
            opening the stream.

        Returns
        -------
        underflowed : bool
            ``True`` if additional output data was inserted after the
            previous call and before this call.

        """
        import numpy as np
        data = np.asarray(data)
        _, dtype = _split(self._dtype)
        _, channels = _split(self._channels)
        if data.ndim > 1 and data.shape[1] != channels:
            raise ValueError('Number of channels must match')
        if data.dtype != dtype:
            raise TypeError('dtype mismatch: {0!r} vs {1!r}'.format(
                data.dtype.name, dtype))
        if not data.flags.c_contiguous:
            raise TypeError('data must be C-contiguous')
        return RawOutputStream.write(self, data)


class Stream(InputStream, OutputStream):
    """Stream for input and output.  See __init__()."""

    def __init__(self, samplerate=None, blocksize=None,
                 device=None, channels=None, dtype=None, latency=None,
                 extra_settings=None, callback=None, finished_callback=None,
                 clip_off=None, dither_off=None, never_drop_input=None,
                 prime_output_buffers_using_stream_callback=None):
        """Open a stream for input and output.

        To open an input-only or output-only stream use `InputStream` or
        `OutputStream`, respectively.  If you want to handle audio data
        as buffer objects instead of NumPy arrays, use `RawStream`,
        `RawInputStream` or `RawOutputStream`.

        A single stream can provide multiple channels of real-time
        streaming audio input and output to a client application.  A
        stream provides access to audio hardware represented by one or
        more devices.  Depending on the underlying Host API, it may be
        possible to open multiple streams using the same device, however
        this behavior is implementation defined.  Portable applications
        should assume that a device may be simultaneously used by at
        most one stream.

        The arguments *device*, *channels*, *dtype* and *latency* can be
        either single values (which will be used for both input and
        output parameters) or pairs of values (where the first one is
        the value for the input and the second one for the output).

        All arguments are optional, the values for unspecified
        parameters are taken from the `default` object.
        If one of the values of a parameter pair is ``None``, the
        corresponding value from `default` will be used instead.

        The created stream is inactive (see `active`, `stopped`).
        It can be started with `start()`.

        Every stream object is also a
        :ref:`context manager <python:context-managers>`, i.e. it can be
        used in a :ref:`with statement <python:with>` to automatically
        call `start()` in the beginning of the statement and `stop()`
        and `close()` on exit.

        Parameters
        ----------
        samplerate : float, optional
            The desired sampling frequency (for both input and output).
            The default value can be changed with `default.samplerate`.
        blocksize : int, optional
            The number of frames passed to the stream callback function,
            or the preferred block granularity for a blocking read/write
            stream.
            The special value ``blocksize=0`` (which is the default) may
            be used to request that the stream callback will receive an
            optimal (and possibly varying) number of frames based on
            host requirements and the requested latency settings.
            The default value can be changed with `default.blocksize`.

            .. note:: With some host APIs, the use of non-zero
               *blocksize* for a callback stream may introduce an
               additional layer of buffering which could introduce
               additional latency.  PortAudio guarantees that the
               additional latency will be kept to the theoretical
               minimum however, it is strongly recommended that a
               non-zero *blocksize* value only be used when your
               algorithm requires a fixed number of frames per stream
               callback.
        device : int or str or pair thereof, optional
            Device index(es) or query string(s) specifying the device(s)
            to be used.  The default value(s) can be changed with
            `default.device`.
        channels : int or pair of int, optional
            The number of channels of sound to be delivered to the
            stream callback or accessed by `read()` or `write()`.  It
            can range from 1 to the value of ``'max_input_channels'`` or
            ``'max_output_channels'`` in the dict returned by
            `query_devices()`.  By default, the maximum possible number
            of channels for the selected device is used (which may not
            be what you want; see `query_devices()`).  The default
            value(s) can be changed with `default.channels`.
        dtype : str or numpy.dtype or pair thereof, optional
            The sample format of the `numpy.ndarray` provided to the
            stream callback, `read()` or `write()`.
            It may be any of *float32*, *int32*, *int16*, *int8*,
            *uint8*. See `numpy.dtype`.
            The *float64* data type is not supported, this is only
            supported for convenience in `play()`/`rec()`/`playrec()`.
            The packed 24 bit format ``'int24'`` is only supported in
            the "raw" stream classes, see `RawStream`.  The default
            value(s) can be changed with `default.dtype`.
        latency : float or {'low', 'high'} or pair thereof, optional
            The desired latency in seconds.  The special values
            ``'low'`` and ``'high'`` (latter being the default) select
            the default low and high latency, respectively (see
            `query_devices()`).  The default value(s) can be changed
            with `default.latency`.
            Where practical, implementations should configure their
            latency based on this parameter, otherwise they may choose
            the closest viable latency instead.  Unless the suggested
            latency is greater than the absolute upper limit for the
            device, implementations should round the *latency* up to the
            next practical value -- i.e. to provide an equal or higher
            latency  wherever possible.  Actual latency values for an
            open stream may be retrieved using the `latency` attribute.
        extra_settings : settings object or pair thereof, optional
            This can be used for host-API-specific input/output
            settings.  See `default.extra_settings`.
        callback : callable, optional
            User-supplied function to consume, process or generate audio
            data in response to requests from an `active` stream.
            When a stream is running, PortAudio calls the stream
            callback periodically.  The callback function is responsible
            for processing and filling input and output buffers,
            respectively.

            If no *callback* is given, the stream will be opened in
            "blocking read/write" mode.  In blocking mode, the client
            can receive sample data using `read()` and write sample
            data using `write()`, the number of frames that may be
            read or written without blocking is returned by
            `read_available` and `write_available`, respectively.

            The callback must have this signature::

                callback(indata: ndarray, outdata: ndarray, frames: int,
                         time: CData, status: CallbackFlags) -> None

            The first and second argument are the input and output
            buffer, respectively, as two-dimensional `numpy.ndarray`
            with one column per channel (i.e.  with a shape of
            ``(frames, channels)``) and with a data type specified by
            `dtype`.
            The output buffer contains uninitialized data and the
            *callback* is supposed to fill it with proper audio data.
            If no data is available, the buffer should be filled with
            zeros (e.g. by using ``outdata.fill(0)``).

            .. note:: In Python, assigning to an identifier merely
               re-binds the identifier to another object, so this *will
               not work* as expected::

                   outdata = my_data  # Don't do this!

               To actually assign data to the buffer itself, you can use
               indexing, e.g.::

                   outdata[:] = my_data

               ... which fills the whole buffer, or::

                   outdata[:, 1] = my_channel_data

               ... which only fills one channel.

            The third argument holds the number of frames to be
            processed by the stream callback.  This is the same as the
            length of the input and output buffers.

            The forth argument provides a CFFI structure with
            timestamps indicating the ADC capture time of the first
            sample in the input buffer (``time.inputBufferAdcTime``),
            the DAC output time of the first sample in the output buffer
            (``time.outputBufferDacTime``) and the time the callback was
            invoked (``time.currentTime``).
            These time values are expressed in seconds and are
            synchronised with the time base used by `time` for the
            associated stream.

            The fifth argument is a `CallbackFlags` instance indicating
            whether input and/or output buffers have been inserted or
            will be dropped to overcome underflow or overflow
            conditions.

            If an exception is raised in the *callback*, it will not be
            called again.  If `CallbackAbort` is raised, the stream will
            finish as soon as possible.  If `CallbackStop` is raised,
            the stream will continue until all buffers generated by the
            callback have been played.  This may be useful in
            applications such as soundfile players where a specific
            duration of output is required.  If another exception is
            raised, its traceback is printed to `sys.stderr`.
            Exceptions are *not* propagated to the main thread, i.e. the
            main Python program keeps running as if nothing had
            happened.

            .. note:: The *callback* must always fill the entire output
               buffer, no matter if or which exceptions are raised.

            If no exception is raised in the *callback*, it
            automatically continues to be called until `stop()`,
            `abort()` or `close()` are used to stop the stream.

            The PortAudio stream callback runs at very high or real-time
            priority.  It is required to consistently meet its time
            deadlines.  Do not allocate memory, access the file system,
            call library functions or call other functions from the
            stream callback that may block or take an unpredictable
            amount of time to complete.  With the exception of
            `cpu_load` it is not permissible to call PortAudio API
            functions from within the stream callback.

            In order for a stream to maintain glitch-free operation the
            callback must consume and return audio data faster than it
            is recorded and/or played.  PortAudio anticipates that each
            callback invocation may execute for a duration approaching
            the duration of *frames* audio frames at the stream's
            sampling frequency.  It is reasonable to expect to be able
            to utilise 70% or more of the available CPU time in the
            PortAudio callback.  However, due to buffer size adaption
            and other factors, not all host APIs are able to guarantee
            audio stability under heavy CPU load with arbitrary fixed
            callback buffer sizes.  When high callback CPU utilisation
            is required the most robust behavior can be achieved by
            using ``blocksize=0``.
        finished_callback : callable, optional
            User-supplied function which will be called when the stream
            becomes inactive (i.e. once a call to `stop()` will not
            block).

            A stream will become inactive after the stream callback
            raises an exception or when `stop()` or `abort()` is called.
            For a stream providing audio output, if the stream callback
            raises `CallbackStop`, or `stop()` is called, the stream
            finished callback will not be called until all generated
            sample data has been played.  The callback must have this
            signature::

                finished_callback() -> None

        clip_off : bool, optional
            See `default.clip_off`.
        dither_off : bool, optional
            See `default.dither_off`.
        never_drop_input : bool, optional
            See `default.never_drop_input`.
        prime_output_buffers_using_stream_callback : bool, optional
            See `default.prime_output_buffers_using_stream_callback`.

        """

        def callback_wrapper(iptr, optr, frames, time, status, _):
            ichannels, ochannels = self._channels
            idtype, odtype = self._dtype
            isize, osize = self._samplesize
            ibuffer = _buffer(iptr, frames, ichannels, isize)
            obuffer = _buffer(optr, frames, ochannels, osize)
            idata = _array(ibuffer, ichannels, idtype)
            odata = _array(obuffer, ochannels, odtype)
            return _wrap_callback(callback, idata, odata, frames, time, status)

        _StreamBase.__init__(
            self, 'duplex', samplerate, blocksize, device, channels, dtype,
            latency, extra_settings, callback and callback_wrapper,
            finished_callback, clip_off, dither_off, never_drop_input,
            prime_output_buffers_using_stream_callback)


class DeviceList(tuple):
    """A list with information about all available audio devices.

    This class is not meant to be instantiated by the user.
    Instead, it is returned by `query_devices()`.
    It contains a dictionary for each available device, holding the keys
    described in `query_devices()`.

    This class has a special string representation that is shown as
    return value of `query_devices()` if used in an interactive
    Python session.  It will also be shown when using the :func:`print`
    function.  Furthermore, it can be obtained with :func:`repr` and
    :class:`str() <str>`.

    """

    __slots__ = ()

    def __repr__(self):
        idev, odev = [
            dev if isinstance(dev, int) else _get_device_id(dev, kind)
            for kind, dev in zip(('input', 'output'), default.device)
        ]
        digits = len(str(_lib.Pa_GetDeviceCount() - 1))
        hostapi_names = [hostapi['name'] for hostapi in query_hostapis()]
        text = '\n'.join(
            u'{mark} {idx:{dig}} {name}, {ha} ({ins} in, {outs} out)'.format(
                mark=(' ', '>', '<', '*')[(idx == idev) + 2 * (idx == odev)],
                idx=idx,
                dig=digits,
                name=info['name'],
                ha=hostapi_names[info['hostapi']],
                ins=info['max_input_channels'],
                outs=info['max_output_channels'])
            for idx, info in enumerate(self))
        if _sys.version_info.major < 3:
            return text.encode(_sys.stdout.encoding or 'utf-8')
        return text


class CallbackFlags(object):
    """Flag bits for the *status* argument to a stream *callback*.

    See Also
    --------
    Stream

    Examples
    --------
    This can be used to collect the errors of multiple *status* objects:

    >>> import sounddevice as sd
    >>> errors = sd.CallbackFlags()
    >>> errors |= status1
    >>> errors |= status2
    >>> errors |= status3
    >>> # and so on ...
    >>> errors.input_overflow
    True

    """

    __slots__ = '_flags'

    def __init__(self, flags=0x0):
        self._flags = flags

    def __repr__(self):
        flags = str(self)
        if not flags:
            flags = 'no flags set'
        return '<sounddevice.CallbackFlags: {0}>'.format(flags)

    def __str__(self):
        return ', '.join(name.replace('_', ' ') for name in dir(self)
                         if not name.startswith('_') and getattr(self, name))

    def __bool__(self):
        return bool(self._flags)

    __nonzero__ = __bool__  # For Python 2.x

    def __ior__(self, other):
        if not isinstance(other, CallbackFlags):
            return NotImplemented
        self._flags |= other._flags
        return self

    @property
    def input_underflow(self):
        """Input underflow.

        In a stream opened with ``blocksize=0``, indicates that input
        data is all silence (zeros) because no real data is available.
        In a stream opened with a non-zero *blocksize*, it indicates
        that one or more zero samples have been inserted into the input
        buffer to compensate for an input underflow.

        """
        return self._hasflag(_lib.paInputUnderflow)

    @property
    def input_overflow(self):
        """Input overflow.

        In a stream opened with ``blocksize=0``, indicates that data
        prior to the first sample of the input buffer was discarded due
        to an overflow, possibly because the stream callback is using
        too much CPU time.  Otherwise indicates that data prior to one
        or more samples in the input buffer was discarded.

        """
        return self._hasflag(_lib.paInputOverflow)

    @property
    def output_underflow(self):
        """Output underflow.

        Indicates that output data (or a gap) was inserted, possibly
        because the stream callback is using too much CPU time.

        """
        return self._hasflag(_lib.paOutputUnderflow)

    @property
    def output_overflow(self):
        """Output overflow.

        Indicates that output data will be discarded because no room is
        available.

        """
        return self._hasflag(_lib.paOutputOverflow)

    @property
    def priming_output(self):
        """Priming output.

        Some of all of the output data will be used to prime the stream,
        input data may be zero.

        """
        return self._hasflag(_lib.paPrimingOutput)

    def _hasflag(self, flag):
        """Helper function to check a given flag."""
        return bool(self._flags & flag)


class _InputOutputPair(object):
    """Parameter pairs for device, channels, dtype and latency."""

    _indexmapping = {'input': 0, 'output': 1}

    def __init__(self, parent, default_attr):
        self._pair = [None, None]
        self._parent = parent
        self._default_attr = default_attr

    def __getitem__(self, index):
        index = self._indexmapping.get(index, index)
        value = self._pair[index]
        if value is None:
            value = getattr(self._parent, self._default_attr)[index]
        return value

    def __setitem__(self, index, value):
        index = self._indexmapping.get(index, index)
        self._pair[index] = value

    def __repr__(self):
        return '[{0[0]!r}, {0[1]!r}]'.format(self)


class default(object):
    """Get/set defaults for the *sounddevice* module.

    The attributes `device`, `channels`, `dtype`, `latency` and
    `extra_settings` accept single values which specify the given
    property for both input and output.  However, if the property
    differs between input and output, pairs of values can be used, where
    the first value specifies the input and the second value specifies
    the output.  All other attributes are always single values.

    Examples
    --------

    >>> import sounddevice as sd
    >>> sd.default.samplerate = 48000
    >>> sd.default.dtype
    ['float32', 'float32']

    Different values for input and output:

    >>> sd.default.channels = 1, 2

    A single value sets both input and output at the same time:

    >>> sd.default.device = 5
    >>> sd.default.device
    [5, 5]

    An attribute can be set to the "factory default" by assigning
    ``None``:

    >>> sd.default.samplerate = None
    >>> sd.default.device = None, 4

    Use `reset()` to reset all attributes:

    >>> sd.default.reset()

    """
    _pairs = 'device', 'channels', 'dtype', 'latency', 'extra_settings'
    # The class attributes listed in _pairs are only provided here for static
    # analysis tools and for the docs.  They're overwritten in __init__().
    device = None, None
    """Index or query string of default input/output device.

    If not overwritten, this is queried from PortAudio.

    If a string is given, the device is selected which contains all
    space-separated parts in the right order.  Each device string
    contains the name of the corresponding host API in the end.
    The string comparison is case-insensitive.

    See Also
    --------
    :func:`query_devices`

    """
    channels = _default_channels = None, None
    """Number of input/output channels.

    The maximum number of channels for a given device can be found out
    with `query_devices()`.

    """
    dtype = _default_dtype = 'float32', 'float32'
    """Data type used for input/output samples.

    The types ``'float32'``, ``'int32'``, ``'int16'``, ``'int8'`` and
    ``'uint8'`` can be used for all streams and functions.
    Additionally, `play()`, `rec()` and `playrec()` support
    ``'float64'`` (for convenience, data is merely converted from/to
    ``'float32'``) and `RawInputStream`, `RawOutputStream` and
    `RawStream` support ``'int24'`` (packed 24 bit format, which is
    *not* supported in NumPy!).

    If NumPy is available, the corresponding `numpy.dtype` objects can
    be used as well.

    The floating point representations ``'float32'`` and ``'float64'``
    use +1.0 and -1.0 as the maximum and minimum values, respectively.
    ``'uint8'`` is an unsigned 8 bit format where 128 is considered
    "ground".

    """
    latency = _default_latency = 'high', 'high'
    """Suggested input/output latency in seconds.

    The special values ``'low'`` and ``'high'`` can be used to select
    the default low/high latency of the chosen device.
    ``'high'`` is typically more robust (i.e. buffer under-/overflows
    are less likely), but the latency may be too large for interactive
    applications.

    See Also
    --------
    :func:`query_devices`

    """
    extra_settings = _default_extra_settings = None, None
    """Host-API-specific input/output settings.

    See Also
    --------
    AsioSettings, WasapiSettings

    """
    samplerate = None
    """Sampling frequency in Hertz (= frames per second).

    See Also
    --------
    :func:`query_devices`

    """
    blocksize = _lib.paFramesPerBufferUnspecified
    """See the *blocksize* argument of `Stream`."""
    clip_off = False
    """Disable clipping.

    Set to ``True`` to disable default clipping of out of range samples.

    """
    dither_off = False
    """Disable dithering.

    Set to ``True`` to disable default dithering.

    """
    never_drop_input = False
    """Set behavior for input overflow of full-duplex streams.

    Set to ``True`` to request that where possible a full duplex stream
    will not discard overflowed input samples without calling the stream
    callback.  This flag is only valid for full-duplex callback streams
    (i.e. only `Stream` and `RawStream` and only if *callback* was
    specified; this includes `playrec()`) and only when used in
    combination with ``blocksize=0`` (the default).
    Using this flag incorrectly results in an error being raised.

    """
    prime_output_buffers_using_stream_callback = False
    """How to fill initial output buffers.

    Set to ``True`` to call the stream callback to fill initial output
    buffers, rather than the default behavior of priming the buffers
    with zeros (silence).  This flag has no effect for input-only
    (`InputStream` and `RawInputStream`) and blocking read/write streams
    (i.e. if *callback* wasn't specified).

    """

    def __init__(self):
        for attr in self._pairs:
            # __setattr__() must be avoided here
            vars(self)[attr] = _InputOutputPair(self, '_default_' + attr)

    def __setattr__(self, name, value):
        """Only allow setting existing attributes."""
        if name in self._pairs:
            getattr(self, name)._pair[:] = _split(value)
        elif name in dir(self) and name != 'reset':
            object.__setattr__(self, name, value)
        else:
            raise AttributeError(
                "'default' object has no attribute " + repr(name))

    @property
    def _default_device(self):
        return (_lib.Pa_GetDefaultInputDevice(),
                _lib.Pa_GetDefaultOutputDevice())

    @property
    def hostapi(self):
        """Index of the default host API (read-only)."""
        return _check(_lib.Pa_GetDefaultHostApi())

    def reset(self):
        """Reset all attributes to their "factory default"."""
        vars(self).clear()
        self.__init__()

if not hasattr(_ffi, 'I_AM_FAKE'):
    # This object shadows the 'default' class, except when building the docs.
    default = default()


class PortAudioError(Exception):
    """This exception will be raised on PortAudio errors."""


class CallbackStop(Exception):
    """Exception to be raised by the user to stop callback processing.

    If this is raised in the stream callback, the callback will not be
    invoked anymore (but all pending audio buffers will be played).

    See Also
    --------
    CallbackAbort, :meth:`Stream.stop`, Stream

    """


class CallbackAbort(Exception):
    """Exception to be raised by the user to abort callback processing.

    If this is raised in the stream callback, all pending buffers are
    discarded and the callback will not be invoked anymore.

    See Also
    --------
    CallbackStop, :meth:`Stream.abort`, Stream

    """


class AsioSettings(object):

    def __init__(self, channel_selectors):
        """ASIO-specific input/output settings.

        Objects of this class can be used as *extra_settings* argument
        to `Stream()` (and variants) or as `default.extra_settings`.

        Parameters
        ----------
        channel_selectors : list of int
            Support for opening only specific channels of an ASIO
            device.  *channel_selectors* is a list of integers
            specifying the (zero-based) channel numbers to use.
            The length of *channel_selectors* must match the
            corresponding *channels* parameter of `Stream()` (or
            variants), otherwise a crash may result.
            The values in the selectors array must specify channels
            within the range of supported channels.

        Examples
        --------
        Setting output channels when calling `play()`:

        >>> import sounddevice as sd
        >>> asio_out = sd.AsioSettings(channel_selectors=[12, 13])
        >>> sd.play(..., extra_settings=asio_out)

        Setting default output channels:

        >>> sd.default.extra_settings = asio_out
        >>> sd.play(...)

        Setting input channels as well:

        >>> asio_in = sd.AsioSettings(channel_selectors=[8])
        >>> sd.default.extra_settings = asio_in, asio_out
        >>> sd.playrec(..., channels=1, ...)

        """
        if isinstance(channel_selectors, int):
            raise TypeError('channel_selectors must be a list or tuple')
        # int array must be kept alive!
        self._selectors = _ffi.new('int[]', channel_selectors)
        self._streaminfo = _ffi.new('PaAsioStreamInfo*', dict(
            size=_ffi.sizeof('PaAsioStreamInfo'),
            hostApiType=_lib.paASIO,
            version=1,
            flags=_lib.paAsioUseChannelSelectors,
            channelSelectors=self._selectors))


class WasapiSettings(object):

    def __init__(self, exclusive=False):
        """WASAPI-specific input/output settings.

        Objects of this class can be used as *extra_settings* argument
        to `Stream()` (and variants) or as `default.extra_settings`.
        They can also be used in `check_input_settings()` and
        `check_output_settings()`.

        Parameters
        ----------
        exclusive : bool
            Exclusive mode allows to deliver audio data directly to
            hardware bypassing software mixing.

        Examples
        --------
        Setting exclusive mode when calling `play()`:

        >>> import sounddevice as sd
        >>> wasapi_exclusive = sd.WasapiSettings(exclusive=True)
        >>> sd.play(..., extra_settings=wasapi_exclusive)

        Setting exclusive mode as default:

        >>> sd.default.extra_settings = wasapi_exclusive
        >>> sd.play(...)

        """
        flags = 0x0
        if exclusive:
            flags |= _lib.paWinWasapiExclusive
        self._streaminfo = _ffi.new('PaWasapiStreamInfo*', dict(
            size=_ffi.sizeof('PaWasapiStreamInfo'),
            hostApiType=_lib.paWASAPI,
            version=1,
            flags=flags,
        ))


class _CallbackContext(object):
    """Helper class for re-use in play()/rec()/playrec() callbacks."""

    blocksize = None
    data = None
    frame = 0
    input_channels = output_channels = None
    input_dtype = output_dtype = None
    input_mapping = output_mapping = None
    silent_channels = None

    def __init__(self, loop=False):
        import threading
        try:
            import numpy
            assert numpy  # avoid "imported but unused" message (W0611)
        except ImportError:
            raise ImportError(
                'NumPy must be installed for play()/rec()/playrec()')
        self.loop = loop
        self.event = threading.Event()
        self.status = CallbackFlags()

    def check_data(self, data, mapping, device):
        """Check data and output mapping."""
        import numpy as np
        data = np.asarray(data)
        if data.ndim < 2:
            data = data.reshape(-1, 1)
        frames, channels = data.shape
        dtype = _check_dtype(data.dtype)
        mapping_is_explicit = mapping is not None
        mapping, channels = _check_mapping(mapping, channels)
        if data.shape[1] == 1:
            pass  # No problem, mono data is duplicated into arbitrary channels
        elif data.shape[1] != len(mapping):
            raise ValueError(
                'number of output channels != size of output mapping')
        # Apparently, some PortAudio host APIs duplicate mono streams to the
        # first two channels, which is unexpected when specifying mapping=[1].
        # In this case, we play silence on the second channel, but only if the
        # device actually supports a second channel:
        if (mapping_is_explicit and np.array_equal(mapping, [0]) and
               query_devices(device, 'output')['max_output_channels'] >= 2):
            channels = 2
        silent_channels = np.setdiff1d(np.arange(channels), mapping)
        if len(mapping) + len(silent_channels) != channels:
            raise ValueError('each channel may only appear once in mapping')

        self.data = data
        self.output_channels = channels
        self.output_dtype = dtype
        self.output_mapping = mapping
        self.silent_channels = silent_channels
        return frames

    def check_out(self, out, frames, channels, dtype, mapping):
        """Check out, frames, channels, dtype and input mapping."""
        import numpy as np
        if out is None:
            if frames is None:
                raise TypeError('frames must be specified')
            if channels is None:
                channels = default.channels['input']
            if channels is None:
                if mapping is None:
                    raise TypeError(
                        'Unable to determine number of input channels')
                else:
                    channels = len(np.atleast_1d(mapping))
            if dtype is None:
                dtype = default.dtype['input']
            out = np.empty((frames, channels), dtype, order='C')
        else:
            frames, channels = out.shape
            dtype = out.dtype
        dtype = _check_dtype(dtype)
        mapping, channels = _check_mapping(mapping, channels)
        if out.shape[1] != len(mapping):
            raise ValueError(
                'number of input channels != size of input mapping')

        self.out = out
        self.input_channels = channels
        self.input_dtype = dtype
        self.input_mapping = mapping
        return frames

    def callback_enter(self, status, data):
        """Check status and blocksize."""
        self.status |= status
        self.blocksize = min(self.frames - self.frame, len(data))

    def read_indata(self, indata):
        # We manually iterate over each channel in mapping because
        # numpy.take(..., out=...) has a bug:
        # https://github.com/numpy/numpy/pull/4246.
        # Note: using indata[:blocksize, mapping] (a.k.a. 'fancy' indexing)
        # would create unwanted copies (and probably memory allocations).
        for target, source in enumerate(self.input_mapping):
            # If out.dtype is 'float64', 'float32' data is "upgraded" here:
            self.out[self.frame:self.frame + self.blocksize, target] = \
                indata[:self.blocksize, source]

    def write_outdata(self, outdata):
        # 'float64' data is cast to 'float32' here:
        outdata[:self.blocksize, self.output_mapping] = \
            self.data[self.frame:self.frame + self.blocksize]
        outdata[:self.blocksize, self.silent_channels] = 0
        if self.loop and self.blocksize < len(outdata):
            self.frame = 0
            outdata = outdata[self.blocksize:]
            self.blocksize = min(self.frames, len(outdata))
            self.write_outdata(outdata)
        else:
            outdata[self.blocksize:] = 0

    def callback_exit(self):
        if not self.blocksize:
            raise CallbackAbort
        self.frame += self.blocksize

    def finished_callback(self):
        self.event.set()

    def start_stream(self, StreamClass, samplerate, channels, dtype, callback,
                     blocking, **kwargs):
        stop()  # Stop previous playback/recording
        self.stream = StreamClass(samplerate=samplerate,
                                  channels=channels,
                                  dtype=dtype,
                                  callback=callback,
                                  finished_callback=self.finished_callback,
                                  **kwargs)
        self.stream.start()
        global _last_callback
        _last_callback = self
        if blocking:
            self.wait()

    def wait(self):
        """Wait for finished_callback.

        Can be interrupted with a KeyboardInterrupt.

        """
        try:
            self.event.wait()
        finally:
            self.stream.close()
        return self.status if self.status else None


def _check_mapping(mapping, channels):
    """Check mapping, obtain channels."""
    import numpy as np
    if mapping is None:
        mapping = np.arange(channels)
    else:
        mapping = np.atleast_1d(mapping)
        if mapping.min() < 1:
            raise ValueError('channel numbers must not be < 1')
        channels = mapping.max()
        mapping -= 1  # channel numbers start with 1
    return mapping, channels


def _check_dtype(dtype):
    """Check dtype."""
    import numpy as np
    dtype = np.dtype(dtype).name
    if dtype in _sampleformats:
        pass
    elif dtype == 'float64':
        dtype = 'float32'
    else:
        raise TypeError('Unsupported data type: ' + repr(dtype))
    return dtype


def _get_stream_parameters(kind, device, channels, dtype, latency,
                           extra_settings, samplerate):
    """Get parameters for one direction (input or output) of a stream."""
    if device is None:
        device = default.device[kind]
    if channels is None:
        channels = default.channels[kind]
    if dtype is None:
        dtype = default.dtype[kind]
    if latency is None:
        latency = default.latency[kind]
    if extra_settings is None:
        extra_settings = default.extra_settings[kind]
    if samplerate is None:
        samplerate = default.samplerate

    device = _get_device_id(device, kind, raise_on_error=True)
    info = query_devices(device)
    if channels is None:
        channels = info['max_' + kind + '_channels']
    try:
        # If NumPy is available, get canonical dtype name
        dtype = _sys.modules['numpy'].dtype(dtype).name
    except Exception:
        pass  # NumPy not available or invalid dtype (e.g. 'int24') or ...
    try:
        sampleformat = _sampleformats[dtype]
    except KeyError:
        raise ValueError('Invalid ' + kind + ' sample format')
    samplesize = _check(_lib.Pa_GetSampleSize(sampleformat))
    if latency in ('low', 'high'):
        latency = info['default_' + latency + '_' + kind + '_latency']
    if samplerate is None:
        samplerate = info['default_samplerate']
    parameters = _ffi.new('PaStreamParameters*', (
        device, channels, sampleformat, latency,
        extra_settings._streaminfo if extra_settings else _ffi.NULL))
    return parameters, dtype, samplesize, samplerate


def _wrap_callback(callback, *args):
    """Invoke callback function and check for custom exceptions."""
    args = args[:-1] + (CallbackFlags(args[-1]),)
    try:
        callback(*args)
    except CallbackStop:
        return _lib.paComplete
    except CallbackAbort:
        return _lib.paAbort
    return _lib.paContinue


def _buffer(ptr, frames, channels, samplesize):
    """Create a buffer object from a pointer to some memory."""
    return _ffi.buffer(ptr, frames * channels * samplesize)


def _array(buffer, channels, dtype):
    """Create NumPy array from a buffer object."""
    import numpy as np
    data = np.frombuffer(buffer, dtype=dtype)
    data.shape = -1, channels
    return data


def _split(value):
    """Split input/output value into two values."""
    if isinstance(value, str):
        # iterable, but not meant for splitting
        return value, value
    try:
        invalue, outvalue = value
    except TypeError:
        invalue = outvalue = value
    except ValueError:
        raise ValueError('Only single values and pairs are allowed')
    return invalue, outvalue


def _check(err, msg=""):
    """Raise error for non-zero error codes."""
    if err < 0:
        msg += ': ' if msg else ''
        if err == _lib.paUnanticipatedHostError:
            info = _lib.Pa_GetLastHostErrorInfo()
            hostapi = _lib.Pa_HostApiTypeIdToHostApiIndex(info.hostApiType)
            msg += 'Unanticipated host API {0} error {1}: {2!r}'.format(
                hostapi, info.errorCode, _ffi.string(info.errorText).decode())
        else:
            msg += _ffi.string(_lib.Pa_GetErrorText(err)).decode()
        raise PortAudioError(msg)
    return err


def _get_device_id(id_or_query_string, kind, raise_on_error=False):
    """Return device ID given space-separated substrings."""
    assert kind in ('input', 'output', None)

    if id_or_query_string is None:
        id_or_query_string = default.device

    idev, odev = _split(id_or_query_string)
    if kind == 'input':
        id_or_query_string = idev
    elif kind == 'output':
        id_or_query_string = odev
    else:
        if idev == odev:
            id_or_query_string = idev
        else:
            raise ValueError('Input and output device are different: {0!r}'
                             .format(id_or_query_string))

    if isinstance(id_or_query_string, int):
        return id_or_query_string
    device_list = []
    for id, info in enumerate(query_devices()):
        if not kind or info['max_' + kind + '_channels'] > 0:
            hostapi_info = query_hostapis(info['hostapi'])
            device_list.append((id, info['name'], hostapi_info['name']))

    query_string = id_or_query_string.lower()
    substrings = query_string.split()
    matches = []
    exact_device_matches = []
    for id, device_string, hostapi_string in device_list:
        full_string = device_string + ', ' + hostapi_string
        pos = 0
        for substring in substrings:
            pos = full_string.lower().find(substring, pos)
            if pos < 0:
                break
            pos += len(substring)
        else:
            matches.append((id, full_string))
            if device_string.lower() == query_string:
                exact_device_matches.append(id)

    if kind is None:
        kind = 'input/output'  # Just used for error messages

    if not matches:
        if raise_on_error:
            raise ValueError(
                'No ' + kind + ' device matching ' + repr(id_or_query_string))
        else:
            return -1
    if len(matches) > 1:
        if len(exact_device_matches) == 1:
            return exact_device_matches[0]
        if raise_on_error:
            raise ValueError('Multiple ' + kind + ' devices found for ' +
                             repr(id_or_query_string) + ':\n' +
                             '\n'.join('[{0}] {1}'.format(id, name)
                                       for id, name in matches))
        else:
            return -1
    return matches[0][0]


def _initialize():
    """Initialize PortAudio."""
    global _initialized
    _check(_lib.Pa_Initialize(), 'Error initializing PortAudio')
    _initialized += 1


def _terminate():
    """Terminate PortAudio."""
    global _initialized
    _check(_lib.Pa_Terminate(), 'Error terminating PortAudio')
    _initialized -= 1


def _exit_handler():
    assert _initialized >= 0
    while _initialized:
        _terminate()


def _ignore_stderr():
    """Try to forward PortAudio messages from stderr to /dev/null."""
    ffi = _FFI()
    ffi.cdef("""
    /* from stdio.h */
    FILE* fopen(const char* path, const char* mode);
    int fclose(FILE* fp);
    FILE* stderr;  /* GNU C library */
    FILE* __stderrp;  /* Mac OS X */
    """)
    try:
        stdio = ffi.dlopen(None)
        devnull = stdio.fopen(_os.devnull.encode(), b'w')
    except (OSError, AttributeError):
        return
    try:
        stdio.stderr = devnull
    except KeyError:
        try:
            stdio.__stderrp = devnull
        except KeyError:
            stdio.fclose(devnull)


_ignore_stderr()
_atexit.register(_exit_handler)
_initialize()

if __name__ == '__main__':
    print(query_devices())
