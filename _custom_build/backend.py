"""A Thin backend wrapper for setuptools.build_meta

See https://setuptools.pypa.io/en/latest/build_meta.html
"""

from setuptools import build_meta as _orig
from setuptools.build_meta import *
import sounddevice_build
import os
import platform
import shutil

sounddevice_build.main()

DARWIN = "Darwin"
WINDOWS = "Windows"
MACOSX_VERSIONS = ["maccosx_10_6_x86_64", "macosx_10_6_universal2"]


def get_platform_specific_wheel_name() -> str:
    """Return the platform specific wheel name."""
    current_platform = os.environ.get("PYTHON_SOUNDDEVICE_PLATFORM", platform.system())
    architecture = os.environ.get("PYTHON_SOUNDDEVICE_ARCHITECTURE", platform.architecture()[0])
    oses = "any"

    if current_platform == DARWIN:
        oses = ".".join(MACOSX_VERSIONS)
    elif current_platform == WINDOWS:
        oses = "win32" if architecture == "32bit" else "win_amd64"

    with open("VERSION", "r") as f:
        version = f.read().strip()

    return f"sounddevice-{version}-py3-none-{oses}.whl"


def prepare_meta_for_build_wheel(config_settings=None):
    """This function may be used in the future to customize platform specific portaudio libraries."""
    return _orig.prepare_metadata_for_build_wheel(config_settings=config_settings)


def get_requires_for_build_wheel(config_settings=None):
    return _orig.get_requires_for_build_wheel(config_settings=config_settings)


def build_wheel(wheel_directory, config_settings=None, metadata_directory=None):
    """Intercept the build wheel function and copy the wheel to a platform specific name.

    We build the wheel as ususal for the package but intercept the output so that we can rename it.
    """

    wheel_file = _orig.build_wheel(wheel_directory, config_settings=config_settings, metadata_directory=metadata_directory)
    old_wheel_path = os.path.join(wheel_directory, wheel_file)
    new_wheel_path = os.path.join(wheel_directory, get_platform_specific_wheel_name())

    shutil.move(old_wheel_path, new_wheel_path)

    return new_wheel_path
