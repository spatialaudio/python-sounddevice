from setuptools import setup

__version__ = "unknown"

# "import" __version__
for line in open("sounddevice.py"):
    if line.startswith("__version__"):
        exec(line)
        break

setup(
    name="sounddevice",
    version=__version__,
    py_modules=["sounddevice"],
    install_requires=["CFFI"],
    extras_require={"NumPy": ["NumPy"]},
    author="Matthias Geier",
    author_email="Matthias.Geier@gmail.com",
    description="Play and Record Sound with Python",
    long_description=open("README.rst").read(),
    license="MIT",
    keywords="sound audio PortAudio play record playrec".split(),
    url="http://python-sounddevice.rtfd.org/",
    platforms="any",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Multimedia :: Sound/Audio",
    ],
)
