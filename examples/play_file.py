#!/usr/bin/env python3
"""Load an audio file into memory and play its contents.

NumPy and the soundfile module (http://PySoundFile.rtfd.io/) must be
installed for this to work.

This example program loads the whole file into memory before starting
playback.
To play very long files, you should use play_long_file.py instead.

"""
import argparse


def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('filename', help='audio file to be played back')
parser.add_argument('-d', '--device', type=int_or_str,
                    help='output device (numeric ID or substring)')
args = parser.parse_args()

try:
    import sounddevice as sd
    import soundfile as sf
    data, fs = sf.read(args.filename, dtype='float32')
    sd.play(data, fs, device=args.device, blocking=True)
    status = sd.get_status()
    if status:
        parser.exit('Error during playback: ' + str(status))
except KeyboardInterrupt:
    parser.exit('\nInterrupted by user')
except Exception as e:
    parser.exit(type(e).__name__ + ': ' + str(e))
