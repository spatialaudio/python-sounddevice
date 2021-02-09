#!/usr/bin/env python3
"""Load an audio file into memory and play its contents.

NumPy and the soundfile module (https://python-soundfile.readthedocs.io/)
must be installed for this to work.

This example program loads the whole file into memory before starting
playback.
To play very long files, you should use play_long_file.py instead.

This example could simply be implemented like this::

    import sounddevice as sd
    import soundfile as sf

    data, fs = sf.read('my-file.wav')
    sd.play(data, fs)
    sd.wait()

... but in this example we show a more low-level implementation
using a callback stream.

"""
import argparse
import threading

import sounddevice as sd
import soundfile as sf


def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text


parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    '-l', '--list-devices', action='store_true',
    help='show list of audio devices and exit')
args, remaining = parser.parse_known_args()
if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])
parser.add_argument(
    'filename', metavar='FILENAME',
    help='audio file to be played back')
parser.add_argument(
    '-d', '--device', type=int_or_str,
    help='output device (numeric ID or substring)')
args = parser.parse_args(remaining)

event = threading.Event()

try:
    data, fs = sf.read(args.filename, always_2d=True)

    current_frame = 0

    def callback(outdata, frames, time, status):
        global current_frame
        if status:
            print(status)
        chunksize = min(len(data) - current_frame, frames)
        outdata[:chunksize] = data[current_frame:current_frame + chunksize]
        if chunksize < frames:
            outdata[chunksize:] = 0
            raise sd.CallbackStop()
        current_frame += chunksize

    stream = sd.OutputStream(
        samplerate=fs, device=args.device, channels=data.shape[1],
        callback=callback, finished_callback=event.set)
    with stream:
        event.wait()  # Wait until playback is finished
except KeyboardInterrupt:
    parser.exit('\nInterrupted by user')
except Exception as e:
    parser.exit(type(e).__name__ + ': ' + str(e))
