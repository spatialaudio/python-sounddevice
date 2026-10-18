"""Regression checks for the NumPy convenience playback callback."""
import unittest
from unittest.mock import patch

import sounddevice as sd

try:
    import numpy as np
except ImportError:
    np = None


@unittest.skipIf(np is None, 'NumPy required for convenience playback')
class PlaybackSilenceTests(unittest.TestCase):

    def test_silent_channels_and_final_padding(self):
        for dtype in ('uint8', 'int16', 'float32', 'float64'):
            for mapping in (None, [1], [2], [3, 1]):
                with self.subTest(dtype=dtype, mapping=mapping):
                    data = np.arange(1, 7).reshape(3, 2).astype(dtype)
                    if dtype.startswith('float'):
                        data /= 10
                    if mapping != [3, 1]:
                        data = data[:, :1]
                    context = sd._CallbackContext()
                    device_info = {'max_output_channels': 2}
                    with patch('sounddevice.query_devices', return_value=device_info):
                        context.frames = context.check_data(data, mapping, None)
                    output = np.empty((8, context.output_channels), context.output_dtype)
                    context.callback_enter(sd.CallbackFlags(), output)
                    context.write_outdata(output)
                    silence = 128 if dtype == 'uint8' else 0
                    np.testing.assert_array_equal(output[3:], silence)
                    np.testing.assert_array_equal(
                        output[:, context.silent_channels], silence)
                    for channel, target in enumerate(context.output_mapping):
                        source = 0 if data.shape[1] == 1 else channel
                        expected = data[:, source].astype(output.dtype)
                        np.testing.assert_array_equal(output[:3, target], expected)

    def test_looped_audio_keeps_unmapped_channels_silent(self):
        for dtype in ('uint8', 'int16', 'float32', 'float64'):
            with self.subTest(dtype=dtype):
                data = np.array([124, 128, 132], dtype=dtype)
                if dtype.startswith('float'):
                    data /= 256
                context = sd._CallbackContext(loop=True)
                context.frames = context.check_data(data, [2], None)
                output = np.empty((8, 2), context.output_dtype)
                context.callback_enter(sd.CallbackFlags(), output)
                context.write_outdata(output)
                np.testing.assert_array_equal(
                    output[:, 1], np.resize(data, 8).astype(output.dtype))
                np.testing.assert_array_equal(
                    output[:, 0], 128 if dtype == 'uint8' else 0)


if __name__ == '__main__':
    unittest.main()
