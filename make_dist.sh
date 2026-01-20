#!/bin/bash

set -euo pipefail

# Create a source distribution and platform-specific wheel distributions.

make_wheel()
{
  # This makes sure that only the appropriate libraries are copied:
  rm -rf build/

  # This builds an sdist (including libs) and uses that to build a wheel:
  PYTHON_SOUNDDEVICE_PLATFORM=$1 PYTHON_SOUNDDEVICE_ARCHITECTURE=${2:-} uv build
}

# This is always 64bit:
make_wheel Darwin

make_wheel Windows 32bit

make_wheel Windows 64bit

make_wheel Windows arm64

# This creates a "pure" wheel and an sdist without libraries:
make_wheel Linux

# NB: "Linux" must be last to get a clean sdist!
