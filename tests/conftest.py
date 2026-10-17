"""Configure synthetic ALSA PCMs before sounddevice initializes PortAudio."""

import json
import random
import os
from pathlib import Path
import sys
import tempfile

import pytest


def pytest_configure(config):
    if sys.platform != 'linux':
        return
    if 'sounddevice' in sys.modules:
        raise pytest.UsageError('Run ALSA tests in a fresh Python process')
    # ALSA_CONFIG_PATH splits on spaces/colons without an escaping syntax.
    temp_root = tempfile.gettempdir()
    if ':' in temp_root or ' ' in temp_root:
        temp_root = '/tmp'
    directory = tempfile.TemporaryDirectory(
        prefix='sounddevice-alsa-', dir=temp_root)
    root = Path(directory.name)
    rng = random.Random(0)
    data = bytes(rng.getrandbits(8) for _ in range(192000))
    (root / 'input.raw').write_bytes(data)
    # This standalone configuration has no hardware PCMs or user includes.
    alsa_config = root / 'alsa.conf'
    alsa_config.write_text(
        """
pcm.null { type null }
# PortAudio 19.6 expects a deferred default/dmix entry during enumeration.
pcm.default { type null }
pcm.test_named {
    type null
    hint { show on description "Synthetic PCM" }
}
pcm.portaudio_file_capture {
    type file
    slave.pcm "null"
    infile %s
    file %s
    format "raw"
}
"""
        % (json.dumps(str(root / 'input.raw'), ensure_ascii=False),
           json.dumps(str(root / 'output.raw'), ensure_ascii=False))
    )
    previous = os.environ.get('ALSA_CONFIG_PATH')
    os.environ['ALSA_CONFIG_PATH'] = str(alsa_config)

    def cleanup():
        if previous is None:
            os.environ.pop('ALSA_CONFIG_PATH', None)
        else:
            os.environ['ALSA_CONFIG_PATH'] = previous
        directory.cleanup()

    config.add_cleanup(cleanup)
    config._alsa_capture_bytes = data


@pytest.fixture
def alsa_capture_bytes(pytestconfig):
    return pytestconfig._alsa_capture_bytes
