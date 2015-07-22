#!/usr/bin/env python3
"""Pass input directly to output.

See https://www.assembla.com/spaces/portaudio/subversion/source/HEAD/portaudio/trunk/test/patest_wire.c

"""
import argparse
import logging

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("-i", "--input-device", type=int, help="input device ID")
parser.add_argument("-o", "--output-device", type=int, help="output device ID")
parser.add_argument("-c", "--channels", type=int, default=2,
                    help="number of channels")
parser.add_argument("-t", "--dtype", help="audio data type")
parser.add_argument("-s", "--samplerate", type=float, help="sampling rate")
parser.add_argument("-b", "--blocksize", type=int, help="block size")
parser.add_argument("-l", "--latency", type=float, help="latency in seconds")
args = parser.parse_args()

try:
    import sounddevice as sd

    callback_status = sd.CallbackFlags()

    def callback(indata, outdata, frames, time, status):
        global callback_status
        callback_status |= status
        outdata[:] = indata

    with sd.Stream(device=(args.input_device, args.output_device),
                   samplerate=args.samplerate, blocksize=args.blocksize,
                   dtype=args.dtype, latency=args.latency,
                   channels=args.channels, callback=callback):
        print("#" * 80)
        print("press Return to quit")
        print("#" * 80)
        input()

    if callback_status:
        logging.warning(str(callback_status))
except BaseException as e:
    # This avoids printing the traceback, especially if Ctrl-C is used.
    raise SystemExit(str(e))
