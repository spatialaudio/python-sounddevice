"""Synthetic Linux integration. No physical microphone acceptance."""

import gc
import sys
import weakref

import pytest

if sys.platform != 'linux':
    pytest.skip('ALSA integration requires Linux', allow_module_level=True)

import sounddevice as sd


@pytest.fixture(autouse=True)
def reset_defaults():
    sd.default.reset()
    yield
    sd.default.reset()


def params(**kwargs):
    return dict(
        samplerate=48000,
        channels=2,
        dtype='int16',
        blocksize=1024,
        latency=4096 / 48000,
        extra_settings=sd.AlsaSettings('null'),
        **kwargs,
    )


def forbid_query(*args, **kwargs):
    raise AssertionError('Device name enumeration was used')


def test_file_pcm_bytes_and_reopen(monkeypatch, alsa_capture_bytes):
    monkeypatch.setattr(sd, 'query_devices', forbid_query)
    expected = alsa_capture_bytes[:16384]
    for _ in range(2):
        options = params()
        options['extra_settings'] = sd.AlsaSettings('portaudio_file_capture')
        with sd.RawInputStream(**options) as stream:
            actual = b''.join(bytes(stream.read(1024)[0]) for _ in range(4))
            assert stream.device == -2
            assert actual == expected


@pytest.mark.parametrize('direction', ['input', 'output'])
def test_format_check_needs_no_latency_or_enumeration(monkeypatch, direction):
    monkeypatch.setattr(sd, 'query_devices', forbid_query)
    getattr(sd, 'check_' + direction + '_settings')(
        channels=2,
        samplerate=48000,
        dtype='int16',
        extra_settings=sd.AlsaSettings('null'),
    )


@pytest.mark.parametrize('device', [0, 'null', 'default'])
def test_conflicting_selector(device):
    with pytest.raises(ValueError, match='conflicts'):
        sd.RawInputStream(**params(device=device))


@pytest.mark.parametrize('value', ['', 'null\x00bad', None, b'null'])
def test_bad_address(value):
    with pytest.raises((TypeError, ValueError)):
        sd.AlsaSettings(value)


@pytest.mark.parametrize(
    'key,value',
    [
        ('channels', None),
        ('channels', 0),
        ('samplerate', None),
        ('samplerate', float('nan')),
        ('latency', 'high'),
        ('latency', float('inf')),
        ('latency', -1),
    ],
)
def test_missing_or_invalid_explicit_parameters(key, value):
    options = params()
    options[key] = value
    with pytest.raises(ValueError, match='AlsaSettings requires'):
        sd.RawInputStream(**options)


def test_missing_pcm_does_not_fallback():
    options = params()
    options['extra_settings'] = sd.AlsaSettings('no_such_pcm_abc')
    with pytest.raises(sd.PortAudioError):
        sd.RawInputStream(**options)
    with sd.RawInputStream(**params()) as stream:
        assert len(stream.read(1024)[0]) == 4096


def test_defaults_and_settings_lifetime(monkeypatch):
    monkeypatch.setattr(sd, 'query_devices', forbid_query)
    sd.default.device = 9876
    sd.default.channels = 2
    sd.default.samplerate = 48000
    sd.default.latency = 4096 / 48000
    settings = sd.AlsaSettings('null')
    ref = weakref.ref(settings)
    sd.default.extra_settings = settings
    stream = sd.RawInputStream(dtype='int16', blocksize=1024)
    sd.default.reset()
    del settings
    gc.collect()
    assert ref() is not None
    with stream:
        assert len(stream.read(1024)[0]) == 4096
    del stream
    gc.collect()
    assert ref() is None


def test_output_and_duplex(monkeypatch):
    monkeypatch.setattr(sd, 'query_devices', forbid_query)
    with sd.RawOutputStream(**params()) as stream:
        stream.write(bytes(4096))
    options = params()
    options['extra_settings'] = (sd.AlsaSettings('null'), sd.AlsaSettings('null'))
    with sd.RawStream(**options) as stream:
        assert stream.device == (-2, -2)
        stream.write(bytes(4096))
        assert len(stream.read(1024)[0]) == 4096


def test_explicit_sentinel(monkeypatch):
    monkeypatch.setattr(sd, 'query_devices', forbid_query)
    with sd.RawInputStream(**params(device=-2)) as stream:
        assert len(stream.read(1024)[0]) == 4096


def test_legacy_index_and_name():
    devices = sd.query_devices()
    index = next(i for i, d in enumerate(devices) if d['name'] == 'test_named')
    for selector in [index, 'test_named']:
        options = params()
        del options['extra_settings']
        options['device'] = selector
        with sd.RawInputStream(**options) as stream:
            assert stream.device == index
            assert len(stream.read(1024)[0]) == 4096


def test_convenience_mapping_is_explicit_error(monkeypatch):
    np = pytest.importorskip('numpy', reason='Convenience API requires NumPy')
    monkeypatch.setattr(sd, 'query_devices', forbid_query)
    with pytest.raises(ValueError, match='OutputStream'):
        sd.play(
            np.zeros(128, dtype='float32'),
            48000,
            mapping=[1],
            extra_settings=sd.AlsaSettings('null'),
            latency=0.05,
        )


@pytest.mark.parametrize(
    'kind,device',
    [
        ('input', (-2, 7)),
        ('input', (None, 7)),
        ('output', (7, -2)),
        ('output', (7, None)),
    ],
)
def test_one_direction_device_pair(kind, device):
    cls = sd.RawInputStream if kind == 'input' else sd.RawOutputStream
    with cls(**params(device=device)) as stream:
        assert stream.device == -2


@pytest.mark.parametrize('key', ['samplerate', 'latency'])
def test_boolean_parameter_rejected(key):
    options = params()
    options[key] = True
    with pytest.raises(ValueError):
        sd.RawInputStream(**options)


def test_mixed_direct_and_indexed_duplex():
    index = next(
        i for i, d in enumerate(sd.query_devices()) if d['name'] == 'test_named'
    )
    options = params()
    options['device'] = (None, index)
    options['extra_settings'] = (sd.AlsaSettings('null'), None)
    with sd.RawStream(**options) as stream:
        assert stream.device == (-2, index)
        stream.write(bytes(4096))
        assert len(stream.read(1024)[0]) == 4096


def test_missing_alsa_backend_error(monkeypatch):
    original = sd._lib

    class NoAlsa:
        paALSA = original.paALSA
        Pa_GetErrorText = original.Pa_GetErrorText
        paUnanticipatedHostError = original.paUnanticipatedHostError

        @staticmethod
        def Pa_HostApiTypeIdToHostApiIndex(api):
            return original.paHostApiNotFound

    monkeypatch.setattr(sd, '_lib', NoAlsa())
    with pytest.raises(sd.PortAudioError, match='ALSA host API is unavailable'):
        sd.AlsaSettings('null')


def test_explicit_none_settings_pair_does_not_reapply_defaults():
    sd.default.extra_settings = sd.AlsaSettings('no_such_pcm_abc')
    sd.check_input_settings(device='test_named', channels=2, samplerate=48000,
                            dtype='int16', extra_settings=(None, None))


def test_mutable_settings_container_lifetime():
    settings = sd.AlsaSettings('null')
    ref = weakref.ref(settings)
    pair = [settings, None]
    options = params()
    options['extra_settings'] = pair
    stream = sd.RawInputStream(**options)
    pair.clear()
    del settings
    gc.collect()
    try:
        assert ref() is not None
        with stream:
            assert len(stream.read(1024)[0]) == 4096
    finally:
        stream.close()
