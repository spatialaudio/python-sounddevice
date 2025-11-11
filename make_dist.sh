#!/bin/bash

set -euo pipefail

# Create a source distribution and platform-specific wheel distributions.

PYTHON=python3

make_wheel()
{
  PYTHON_SOUNDDEVICE_PLATFORM=$1 PYTHON_SOUNDDEVICE_ARCHITECTURE=${2:-} \
    $PYTHON -m build
}

# This is always 64bit:
make_wheel Darwin

make_wheel Windows 32bit

make_wheel Windows 64bit

make_wheel Windows arm64

# This makes sure that the libraries are not copied to the final sdist:
rm -rf sounddevice.egg-info/

# This creates a "pure" wheel:
make_wheel Linux
