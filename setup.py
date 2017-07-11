from setuptools import setup

__version__ = 'unknown'

# "import" __version__
for line in open('src/sounddevice.py'):
    if line.startswith('__version__'):
        exec(line)
        break

setup(
    name='sounddevice',
    version=__version__,
    package_dir={'': 'src'},
    py_modules=['sounddevice'],
    cffi_modules=['sounddevice_build.py:ffibuilder'],
    setup_requires=[
        'CFFI>=1.4.0',
    ],
    install_requires=[
        'CFFI>=1',  # for _cffi_backend
    ],
    zip_safe=True,
    extras_require={'NumPy': ['NumPy']},
    author='Matthias Geier',
    author_email='Matthias.Geier@gmail.com',
    description='Play and Record Sound with Python',
    long_description=open('README.rst').read(),
    license='MIT',
    keywords='sound audio PortAudio play record playrec'.split(),
    url='http://python-sounddevice.readthedocs.io/',
    platforms='any',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Multimedia :: Sound/Audio',
    ],
)
