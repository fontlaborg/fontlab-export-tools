from .utils import read_config
from pathlib import Path
import sys
import subprocess


def make(config_path, command="build"):
    config = read_config(config_path)
    if public_repo_folder := config.get("public_repo_folder", None):
        try:
            result = subprocess.run(
                ["make", command], cwd=public_repo_folder, check=True
            )
        except subprocess.CalledProcessError as e:
            print(f"Error running `make {command}` in `{public_repo_folder}`: {e}")
            result = False
    else:
        print("Error: `public_repo_folder` not in config.")
        result = False
    return result
