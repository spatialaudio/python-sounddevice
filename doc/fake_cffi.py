"""Mock module for Sphinx autodoc."""


class FFI(object):

    NULL = NotImplemented
    I_AM_FAKE = True  # This is used for the documentation of "default"

    def cdef(self, _):
        pass

    def dlopen(self, _):
        return FakeLibrary()


class FakeLibrary(object):

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
