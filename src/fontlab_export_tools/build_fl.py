#!/usr/bin/env python3

from .utils import read_config
from pathlib import Path
import sys
import subprocess


def build_fl(config_path):
    config = read_config(config_path)
    vfpy_path = config.get("vfpy_path", None) or Path(
        Path(__file__).parent / "fontlab_export.vfpy"
    )
    fontlab_path = config.get("fontlab_path", None)
    if sys.platform == "darwin":
        fontlab_path = fontlab_path or Path(
            "/Applications/FontLab 8.app/Contents/MacOS/FontLab 8"
        )
    elif sys.platform == "win32":
        fontlab_path = fontlab_path or Path(
            "C:/Program Files/FontLab/FontLab 8/FontLab8.exe"
        )

    args = [fontlab_path, vfpy_path, config_path]

    result = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Print the app's exit code
    code = result.returncode
    return f"Exported: {config.input_path}\nYou may need to quit FontLab manually."
