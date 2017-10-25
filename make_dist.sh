#!/bin/sh

# Create a source distribution and platform-specific wheel distributions.

PYTHON=python3

make_wheel()
{
  $PYTHON setup.py clean --all
  PYTHON_SOUNDDEVICE_PLATFORM=$1 PYTHON_SOUNDDEVICE_ARCHITECTURE=$2 \
    $PYTHON setup.py bdist_wheel
}

rm -rf src/sounddevice.egg-info/
$PYTHON setup.py clean --all
$PYTHON setup.py sdist

# This creates a "pure" wheel:
make_wheel Linux

# This is always 64bit:
make_wheel Darwin

make_wheel Windows 32bit

make_wheel Windows 64bit

$PYTHON setup.py clean --all
