# trimgmi
# Copyright 2022 David Seaward and contributors
# SPDX-License-Identifier: GPL-3.0-or-later

import string
from dataclasses import dataclass, field
from enum import Enum

from typing import List


# HELPER FUNCTIONS


def split_at_first_whitespace(raw_text: str):

    # this may be that one case where regex is helpful

    p = -1  # pointer
    c = -1  # counter
    while p == -1 and c < len(raw_text) - 1:
        c += 1
        if raw_text[c] in string.whitespace:
            p = c

    if p == -1:
        # target without text
        return raw_text, ""
    else:
        # target and text
        return raw_text[:p], raw_text[p:].strip()


# CORE CLASSES


class LineType(Enum):
    BLANK = 0
    REGULAR = 1
    LINK = 2
    HEADING1 = 31
    HEADING2 = 32
    HEADING3 = 33
    LIST_ITEM = 4
    QUOTE = 5
    PREFORMAT_START = 61
    PREFORMAT_LINE = 62
    PREFORMAT_END = 63

    @staticmethod
    def identify(raw_text: str, preformat: bool):

        # note comments that explain when the order of tests matters

        # test preformatting states first and in order
        if raw_text.startswith("```") and preformat:
            return LineType.PREFORMAT_END

        elif raw_text.startswith("```") and not preformat:
            return LineType.PREFORMAT_START

        elif preformat:
            return LineType.PREFORMAT_LINE

        # test all other states after preformatting
        elif raw_text.strip() == "":
            return LineType.BLANK

        # test headings in descending order of length
        elif raw_text.startswith("###"):
            return LineType.HEADING3

        elif raw_text.startswith("##"):
            return LineType.HEADING2

        elif raw_text.startswith("#"):
            return LineType.HEADING1

        # simple startswith tests
        elif raw_text.startswith("*"):
            return LineType.LIST_ITEM

        elif raw_text.startswith("=>"):
            return LineType.LINK

        elif raw_text.startswith(">"):
            return LineType.QUOTE

        # all other cases are regular text (or not specified)
        else:
            return LineType.REGULAR

    @staticmethod
    def within_preformat(line_type):
        return line_type in [LineType.PREFORMAT_START, LineType.PREFORMAT_LINE]


@dataclass
class Line:
    type: LineType
    text: str
    extra: str

    @staticmethod
    def extract(line_type: LineType, raw_text: str):

        if line_type == LineType.BLANK:
            return Line(LineType.BLANK, "", "")

        elif line_type == LineType.REGULAR:
            return Line(LineType.REGULAR, raw_text.rstrip(), extra="")

        elif line_type == LineType.LINK:
            raw_text = raw_text[2:].strip()  # trim identifier
            target, clean_text = split_at_first_whitespace(raw_text)
            return Line(LineType.LINK, clean_text, extra=target)

        elif line_type == LineType.HEADING1:
            clean_text = raw_text[1:].strip()
            return Line(LineType.HEADING1, clean_text, extra="")

        elif line_type == LineType.HEADING2:
            clean_text = raw_text[2:].strip()
            return Line(LineType.HEADING2, clean_text, extra="")

        elif line_type == LineType.HEADING3:
            clean_text = raw_text[3:].strip()
            return Line(LineType.HEADING3, clean_text, extra="")

        elif line_type == LineType.LIST_ITEM:
            clean_text = raw_text[1:].strip()
            return Line(LineType.LIST_ITEM, clean_text, extra="")

        elif line_type == LineType.QUOTE:
            clean_text = raw_text[1:].strip()
            return Line(LineType.QUOTE, clean_text, extra="")

        elif line_type == LineType.PREFORMAT_START:
            label = raw_text[3:].strip()
            return Line(LineType.PREFORMAT_START, "", extra=label)

        elif line_type == LineType.PREFORMAT_LINE:
            return Line(LineType.PREFORMAT_LINE, raw_text.rstrip(), extra="")

        elif line_type == LineType.PREFORMAT_END:
            return Line(LineType.PREFORMAT_END, "", "")

        else:
            raise RuntimeWarning(f"Line type {line_type} not recognised.")


@dataclass
class Document:
    _lines: List[Line] = field(default_factory=lambda: [])
    _preformat: bool = False

    def append(self, raw_text: str):
        line_type = LineType.identify(raw_text, self._preformat)
        self._preformat = LineType.within_preformat(line_type)
        self._lines.append(Line.extract(line_type, raw_text))

    def emit_line_objects(self, auto_tidy=True):

        # test for empty list
        if len(self._lines) == 0:
            return []

        # test for invalid state
        trailing = LineType.within_preformat(self._lines[-1].type)
        if trailing and not auto_tidy:
            raise RuntimeWarning("Preformat block still open.")

        # yield all lines
        for line in self._lines:
            yield line

        # yield tidy line, if required
        if trailing and auto_tidy:
            yield Line(LineType.PREFORMAT_END, "", "")

    def emit_trim_gmi(self):

        for line in self.emit_line_objects(auto_tidy=True):

            if line.type == LineType.BLANK:
                yield ""

            elif line.type == LineType.REGULAR:
                yield line.text

            elif line.type == LineType.LINK:
                if line.text == "":
                    yield f"=> {line.extra}"
                else:
                    yield f"=> {line.extra} {line.text}"

            elif line.type == LineType.HEADING1:
                yield f"# {line.text}"

            elif line.type == LineType.HEADING2:
                yield f"## {line.text}"

            elif line.type == LineType.HEADING3:
                yield f"### {line.text}"

            elif line.type == LineType.LIST_ITEM:
                yield f"* {line.text}"

            elif line.type == LineType.QUOTE:
                yield f"> {line.text}"

            elif line.type == LineType.PREFORMAT_START:
                if line.extra == "":
                    yield "```"
                else:
                    yield f"```{line.extra}"

            elif line.type == LineType.PREFORMAT_LINE:
                yield line.text

            elif line.type == LineType.PREFORMAT_END:
                yield "```"

            else:
                raise RuntimeWarning(f"Line type {line.type} not recognised.")
