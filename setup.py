import os
import platform
from setuptools import setup

# "import" __version__
__version__ = 'unknown'
for line in open('sounddevice.py'):
    if line.startswith('__version__'):
        exec(line)
        break

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

if libname and os.path.isdir('_sounddevice_data/portaudio-binaries'):
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
    name='sounddevice',
    version=__version__,
    py_modules=['sounddevice'],
    packages=packages,
    package_data=package_data,
    zip_safe=zip_safe,
    python_requires='>=3.7',
    setup_requires=['CFFI>=1.0'],
    install_requires=['CFFI>=1.0'],
    extras_require={'NumPy': ['NumPy']},
    cffi_modules=['sounddevice_build.py:ffibuilder'],
    author='Matthias Geier',
    author_email='Matthias.Geier@gmail.com',
    description='Play and Record Sound with Python',
    long_description=open('README.rst').read(),
    license='MIT',
    keywords='sound audio PortAudio play record playrec'.split(),
    url='http://python-sounddevice.readthedocs.io/',
    project_urls={
        'Source': 'https://github.com/spatialaudio/python-sounddevice',
    },
    platforms='any',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Multimedia :: Sound/Audio',
    ],
    cmdclass=cmdclass,
)
