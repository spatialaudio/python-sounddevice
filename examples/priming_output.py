#!/usr/bin/env python3
"""Test priming output buffer.

See http://www.portaudio.com/docs/proposals/020-AllowCallbackToPrimeStream.html

Note that this is only supported in some of the host APIs.

"""
import sounddevice as sd


def callback(indata, outdata, frames, time, status):
    outdata.fill(0)
    if status.priming_output:
        assert status.input_underflow, 'input underflow flag should be set'
        assert not indata.any(), 'input buffer should be filled with zeros'
        print('Priming output buffer!')
        outdata[0] = 1
    else:
        print('Not priming, I quit!')
        raise sd.CallbackStop


with sd.Stream(channels=2, callback=callback,
               prime_output_buffers_using_stream_callback=True) as stream:
    while stream.active:
        sd.sleep(100)
