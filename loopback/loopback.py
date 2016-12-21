#!/usr/bin/env python3
"""Subset of the PortAudio loopback test.

No automatic scanning.
No ...

"""
import sounddevice as sd

print('PortAudio LoopBack Test')

# TODO default settings

# inputDevice = paNoDevice;
# outputDevice = paNoDevice;
# sampleRate = -1;
# framesPerBuffer = -1;
# inputLatency = -1;
# outputLatency = -1;
# waveFilePath = ".";
# saveBadWaves
# verbose

# TODO arg parsing

# paloopback [-i# -o# -l# -r# -s# -m -w -dDir]
#   -i# - Input device ID. Will scan for loopback cable if not specified.
#   -o# - Output device ID. Will scan for loopback if not specified.
#   -l# - Latency for both input and output in milliseconds.
#   --inputLatency # Input latency in milliseconds.
#   --outputLatency # Output latency in milliseconds.
#   -r# - Sample Rate in Hz.  Will use multiple common rates if not specified.
#   -s# - Size of callback buffer in frames, framesPerBuffer. Will use common values if not specified.
#   -w  - Save bad recordings in a WAV file.
#   -dDir - Path for Directory for WAV files. Default is current directory.
#   -m  - Just test the DSP Math code and not the audio devices.
#   -v  - Verbose reports.

# TODO justMath
# printf("Option -m set so just testing math and not the audio devices.\n");

# TODO PaQa_TestAnalyzer()

# TestSavedWave()
# * Simple test that writes a sawtooth waveform to a file. "test_sawtooth.wav"
# TestSingleMonoTone()
# * Detect a single tone. "exact frequency match"/"wrong frequency"
# TestMixedMonoTones()
# * Mix multiple tones and then detect them. NUM_TONES = 5
# TestDetectPhaseErrors()
# // Detect dropped or added samples in a sine wave recording.
# TestNotchFilter()
# * Generate a tone then knock it out using a filter.
# * Also check using filter slightly off tune to see if some energy gets through.
# TestDetectPops()
# // Detect pops that get back in phase.
# TestInitialSpike()
# * Test analysis when there is a DC offset step before the sine signal.

# TODO TestSampleFormatConversion()

print('PortAudio version number = {}\nPortAudio version text = {!r}'.format(*sd.get_portaudio_version()))
print('=============== PortAudio Devices ========================')
print(sd.query_devices())
# printf( "no devices found.\n" );
# printf( "=============== Detect Loopback ==========================\n" );
# ScanForLoopback(&userOptions);

# TODO PaQa_CheckForLoopBack
# TODO PaQa_AnalyzeLoopbackConnection
# TODO PaQa_SingleLoopBackTest
