#!/usr/bin/env python3

import fire
from pathlib import Path
from .git import clone_or_pull, commit_and_push
from .build_ufo import build_ufo
from .build_fl import build_fl


def main():
    fire.core.Display = lambda lines, out: print(*lines, file=out)
    fire.Fire(
        {
            "build_fl": build_fl,
            "build_ufo": build_ufo,
            "pull": clone_or_pull,
            "push": commit_and_push,
        },
        name="fontlabexp",
    )


if __name__ == "__main__":
    main()
