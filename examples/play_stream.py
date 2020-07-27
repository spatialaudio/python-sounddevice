#!/usr/bin/env python3
"""Play a web stream.

ffmpeg-python (https://github.com/kkroening/ffmpeg-python) has to be installed.

If you don't know a stream URL, try http://icecast.spc.org:8000/longplayer
(see https://longplayer.org/ for a description).

"""
import argparse
import queue
import sys

import ffmpeg
import sounddevice as sd


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
    'url', metavar='URL',
    help='stream URL')
parser.add_argument(
    '-d', '--device', type=int_or_str,
    help='output device (numeric ID or substring)')
parser.add_argument(
    '-b', '--blocksize', type=int, default=1024,
    help='block size (default: %(default)s)')
parser.add_argument(
    '-q', '--buffersize', type=int, default=20,
    help='number of blocks used for buffering (default: %(default)s)')
args = parser.parse_args(remaining)
if args.blocksize == 0:
    parser.error('blocksize must not be zero')
if args.buffersize < 1:
    parser.error('buffersize must be at least 1')

q = queue.Queue(maxsize=args.buffersize)

print('Getting stream information ...')

try:
    info = ffmpeg.probe(args.url)
except ffmpeg.Error as e:
    sys.stderr.buffer.write(e.stderr)
    parser.exit(e)

streams = info.get('streams', [])
if len(streams) != 1:
    parser.exit('There must be exactly one stream available')

stream = streams[0]

if stream.get('codec_type') != 'audio':
    parser.exit('The stream must be an audio stream')

channels = stream['channels']
samplerate = float(stream['sample_rate'])


def callback(outdata, frames, time, status):
    assert frames == args.blocksize
    if status.output_underflow:
        print('Output underflow: increase blocksize?', file=sys.stderr)
        raise sd.CallbackAbort
    assert not status
    try:
        data = q.get_nowait()
    except queue.Empty as e:
        print('Buffer is empty: increase buffersize?', file=sys.stderr)
        raise sd.CallbackAbort from e
    assert len(data) == len(outdata)
    outdata[:] = data


try:
    print('Opening stream ...')
    process = ffmpeg.input(
        args.url
    ).output(
        'pipe:',
        format='f32le',
        acodec='pcm_f32le',
        ac=channels,
        ar=samplerate,
        loglevel='quiet',
    ).run_async(pipe_stdout=True)
    stream = sd.RawOutputStream(
        samplerate=samplerate, blocksize=args.blocksize,
        device=args.device, channels=channels, dtype='float32',
        callback=callback)
    read_size = args.blocksize * channels * stream.samplesize
    print('Buffering ...')
    for _ in range(args.buffersize):
        q.put_nowait(process.stdout.read(read_size))
    print('Starting Playback ...')
    with stream:
        timeout = args.blocksize * args.buffersize / samplerate
        while True:
            q.put(process.stdout.read(read_size), timeout=timeout)
except KeyboardInterrupt:
    parser.exit('\nInterrupted by user')
except queue.Full:
    # A timeout occurred, i.e. there was an error in the callback
    parser.exit(1)
except Exception as e:
    parser.exit(type(e).__name__ + ': ' + str(e))
