#!/usr/bin/env python3
"""Load an audio file and play its contents.

PySoundFile (https://github.com/bastibe/PySoundFile/) has to be installed!

"""
import argparse
import logging

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("filename", help="audio file to be played back")
parser.add_argument("-d", "--device", type=int, help="device ID")
args = parser.parse_args()

try:
    import sounddevice as sd
    import soundfile as sf
    data, fs = sf.read(args.filename, dtype='float32')
    sd.play(data, fs, device=args.device, blocking=True)
    status = sd.get_status()
    if status:
        logging.warning(str(status))
except BaseException as e:
    # This avoids printing the traceback, especially if Ctrl-C is used.
    raise SystemExit(str(e))
