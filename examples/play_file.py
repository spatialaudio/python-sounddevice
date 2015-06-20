#!/usr/bin/env python3
"""Load an audio file and play its contents.

PySoundFile (https://github.com/bastibe/PySoundFile/) has to be installed!

"""
import argparse
import sounddevice as sd
import soundfile as sf
import sys

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("filename", help="audio file to be played back")
parser.add_argument("-d", "--device", type=int, help="device ID")
args = parser.parse_args()

try:
    data, fs = sf.read(args.filename, dtype='float32')
    sd.play(data, fs, device=args.device, blocking=True)
except:
    # This avoids printing the traceback, especially if Ctrl-C is used.
    sys.exit(sys.exc_info()[1])
