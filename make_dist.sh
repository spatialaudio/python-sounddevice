#!/bin/bash

set -euo pipefail

# Create a source distribution and platform-specific wheel distributions.

PYTHON="uv run --locked --with build python"

make_wheel()
{
  # This makes sure that only the appropriate libraries are copied:
  rm -rf sounddevice.egg-info/

  PYTHON_SOUNDDEVICE_PLATFORM=$1 PYTHON_SOUNDDEVICE_ARCHITECTURE=${2:-} \
    $PYTHON -m build
}

# This is always 64bit:
make_wheel Darwin

make_wheel Windows 32bit

make_wheel Windows 64bit

# This creates a "pure" wheel and an sdist without libraries:
make_wheel Linux
