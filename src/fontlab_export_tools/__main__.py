#!/usr/bin/env python3

import fire
from pathlib import Path
from .git import GitHandler
from .build_ufo import build_ufo
from .build_fl import build_fl
from .make import make


def clone_or_pull(config_path):
    git = GitHandler(config_path)
    git.clone_or_pull()


def commit_and_push(config_path):
    git = GitHandler(config_path)
    git.commit_and_push()


def sync(config_path):
    git = GitHandler(config_path)
    git.sync()


def main():
    """
    FontLab Export CLI

    This is the main entry point for the fontlabexp command line
    utility. It uses Fire to parse command line arguments and
    dispatch them to the appropriate functions.

    The following functions are available:

    - build_fl
    - build_ufo
    - make
    - pull
    - push
    - sync
    """
    fire.core.Display = lambda lines, out: print(*lines, file=out)
    fire.Fire(
        {
            "build_fl": build_fl,
            "build_ufo": build_ufo,
            "make": make,
            "pull": clone_or_pull,
            "push": commit_and_push,
            "sync": sync,
        },
        name="fontlabexp",
    )


if __name__ == "__main__":
    main()
