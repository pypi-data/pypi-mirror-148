# trimgmi
# Copyright 2022 David Seaward and contributors
# SPDX-License-Identifier: GPL-3.0-or-later

import sys
from pathlib import Path

from trimgmi.sample import reformat_file


def main():
    if len(sys.argv) != 4:
        raise RuntimeError(
            "Too many/too few arguments.\n"
            "Use `convertgmi <format> <input path> <output path>`.\n"
            "Format can be gmi, md or html."
        )

    output_format = str.upper(sys.argv[1])
    input_path = Path(sys.argv[2])
    output_path = Path(sys.argv[3])
    reformat_file(output_format, input_path, output_path)


if __name__ == "__main__":
    main()
