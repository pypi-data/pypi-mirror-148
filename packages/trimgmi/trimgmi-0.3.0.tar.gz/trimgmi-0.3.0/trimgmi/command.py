# trimgmi
# Copyright 2022 David Seaward and contributors
# SPDX-License-Identifier: GPL-3.0-or-later

import os.path
import sys
from pathlib import Path

from trimgmi.sample import reformat_file


def search_and_trim(base_folder: Path):

    for pattern in ["**/*.gmi", "**/*.gemini"]:
        for file_path in base_folder.glob(pattern):
            reformat_file("GMI", file_path, file_path)


def main():
    if len(sys.argv) != 2:
        raise RuntimeError("Too many/too few arguments.\nUse `trimgmi <path>`")

    base_path = Path(sys.argv[1])

    if os.path.isfile(base_path):
        reformat_file("gmi", base_path, base_path)
    elif os.path.isdir(base_path):
        search_and_trim(base_path)
    else:
        raise RuntimeError(f"Path {base_path} not recognised.")


if __name__ == "__main__":
    main()
