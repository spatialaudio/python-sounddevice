import os
import platform
from setuptools import setup

MACOSX_VERSIONS = '.'.join([
    'macosx_10_6_x86_64',  # for compatibility with pip < v21
    'macosx_10_6_universal2',
])

# environment variables for cross-platform package creation
system = os.environ.get('PYTHON_SOUNDDEVICE_PLATFORM', platform.system())
architecture0 = os.environ.get('PYTHON_SOUNDDEVICE_ARCHITECTURE',
                               platform.architecture()[0])

if system == 'Darwin':
    libname = 'libportaudio.dylib'
elif system == 'Windows':
    libname = 'libportaudio' + architecture0 + '.dll'
    libname_asio = 'libportaudio' + architecture0 + '-asio.dll'
else:
    libname = None

if libname:
    packages = ['_sounddevice_data']
    package_data = {'_sounddevice_data': ['portaudio-binaries/' + libname,
                                          'portaudio-binaries/README.md']}
    if system == 'Windows':
        package_data['_sounddevice_data'].append(
            'portaudio-binaries/' + libname_asio)
    zip_safe = False
else:
    packages = None
    package_data = None
    zip_safe = True

try:
    from wheel.bdist_wheel import bdist_wheel
except ImportError:
    cmdclass = {}
else:
    class bdist_wheel_half_pure(bdist_wheel):
        """Create OS-dependent, but Python-independent wheels."""

        def get_tag(self):
            if system == 'Darwin':
                oses = MACOSX_VERSIONS
            elif system == 'Windows':
                if architecture0 == '32bit':
                    oses = 'win32'
                else:
                    oses = 'win_amd64'
            else:
                oses = 'any'
            return 'py3', 'none', oses

    cmdclass = {'bdist_wheel': bdist_wheel_half_pure}

setup(
    package_dir = {'': 'src'},
    py_modules=['sounddevice'],
    packages=packages,
    package_data=package_data,
    zip_safe=zip_safe,
    cffi_modules=['sounddevice_build.py:ffibuilder'],
    cmdclass=cmdclass,
)
