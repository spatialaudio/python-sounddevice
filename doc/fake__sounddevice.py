"""Mock module for Sphinx autodoc."""


import ctypes.util


old_find_library = ctypes.util.find_library


def new_find_library(name):
    if 'portaudio' in name.lower():
        return NotImplemented
    return old_find_library(name)


# Monkey-patch ctypes to disable searching for PortAudio
ctypes.util.find_library = new_find_library


class ffi:

    NULL = NotImplemented
    I_AM_FAKE = True  # This is used for the documentation of "default"

    def dlopen(self, _):
        return FakeLibrary()


ffi = ffi()


class FakeLibrary:

    # from portaudio.h:

    paFloat32 = paInt32 = paInt24 = paInt16 = paInt8 = paUInt8 = NotImplemented
    paFramesPerBufferUnspecified = 0

    def Pa_Initialize(self):
        return 0

    def Pa_Terminate(self):
        return 0

    # from stdio.h:

    def fopen(*args, **kwargs):
        return NotImplemented

    def fclose(*args):
        pass

    stderr = NotImplemented
