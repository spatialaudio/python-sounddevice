import os
import platform
from setuptools import setup

__version__ = 'unknown'

# "import" __version__
for line in open('sounddevice.py'):
    if line.startswith('__version__'):
        exec(line)
        break

PYTHON_INTERPRETERS = '.'.join([
    'cp26', 'cp27',
    'cp32', 'cp33', 'cp34', 'cp35', 'cp36',
    'pp27',
    'pp32', 'pp33', 'pp34', 'pp35', 'pp36',
])
MACOSX_VERSIONS = '.'.join([
    'macosx_10_6_x86_64',
])

# environment variables for cross-platform package creation
system = os.environ.get('PYTHON_SOUNDDEVICE_PLATFORM', platform.system())
architecture0 = os.environ.get('PYTHON_SOUNDDEVICE_ARCHITECTURE',
                               platform.architecture()[0])

if system == 'Darwin':
    libname = 'libportaudio.dylib'
elif system == 'Windows':
    libname = 'libportaudio' + architecture0 + '.dll'
else:
    libname = None

if libname and os.path.isdir('_sounddevice_data'):
    packages = ['_sounddevice_data']
    package_data = {'_sounddevice_data': [libname, 'README.md']}
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
            pythons = 'py2.py3.' + PYTHON_INTERPRETERS
            if system == 'Darwin':
                oses = MACOSX_VERSIONS
            elif system == 'Windows':
                if architecture0 == '32bit':
                    oses = 'win32'
                else:
                    oses = 'win_amd64'
            else:
                pythons = 'py2.py3'
                oses = 'any'
            return pythons, 'none', oses

    cmdclass = {'bdist_wheel': bdist_wheel_half_pure}

setup(
    name='sounddevice',
    version=__version__,
    py_modules=['sounddevice'],
    packages=packages,
    package_data=package_data,
    zip_safe=zip_safe,
    install_requires=['CFFI>=1.0'],
    extras_require={'NumPy': ['NumPy']},
    author='Matthias Geier',
    author_email='Matthias.Geier@gmail.com',
    description='Play and Record Sound with Python',
    long_description=open('README.rst').read(),
    license='MIT',
    keywords='sound audio PortAudio play record playrec'.split(),
    url='http://python-sounddevice.rtfd.org/',
    platforms='any',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Multimedia :: Sound/Audio',
    ],
    cmdclass=cmdclass,
)
