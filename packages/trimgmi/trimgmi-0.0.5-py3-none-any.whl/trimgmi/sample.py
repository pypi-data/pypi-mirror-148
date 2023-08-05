# trimgmi
# Copyright 2022 David Seaward and contributors
# SPDX-License-Identifier: GPL-3.0-or-later

from pathlib import Path

from trimgmi import Document as GmiDocument
from trimgmi import LineType as GmiLineType


def emit_naive_html(document: GmiDocument):

    # Out of scope:
    # * HTML character encoding
    # * HTML validation

    for line in document.emit_line_objects(auto_tidy=True):

        if line.type == GmiLineType.BLANK:
            yield "<br/>"

        elif line.type == GmiLineType.REGULAR:
            yield f"{line.text}<br />"

        elif line.type == GmiLineType.LINK:
            if line.text == "":
                yield f'<li><a href="{line.extra}">{line.extra}</a></li>'
            else:
                yield f'<li><a href="{line.extra}">{line.text}</a></li>'

        elif line.type == GmiLineType.HEADING1:
            yield f"<h1>{line.text}</h1>"

        elif line.type == GmiLineType.HEADING2:
            yield f"<h2>{line.text}</h2>"

        elif line.type == GmiLineType.HEADING3:
            yield f"<h3>{line.text}</h3>"

        elif line.type == GmiLineType.LIST_ITEM:
            yield f"<li>{line.text}</li>"

        elif line.type == GmiLineType.QUOTE:
            yield f"<blockquote>{line.text}</blockquote>"

        elif line.type == GmiLineType.PREFORMAT_START:
            if line.extra == "":
                yield "<pre>"
            else:
                yield f'<pre class="{line.extra}">'

        elif line.type == GmiLineType.PREFORMAT_LINE:
            yield line.text

        elif line.type == GmiLineType.PREFORMAT_END:
            yield "</pre>"

        else:
            raise RuntimeWarning(f"Line type {line.type} not recognised.")


def emit_commonmark(document: GmiDocument):

    for line in document.emit_line_objects(auto_tidy=True):

        if line.type == GmiLineType.BLANK:
            yield ""

        elif line.type == GmiLineType.REGULAR:
            yield line.text

        elif line.type == GmiLineType.LINK:
            if line.text == "":
                yield f"* <{line.extra}>"
            else:
                yield f"* [{line.text}]({line.extra})"

        elif line.type == GmiLineType.HEADING1:
            yield f"# {line.text}"

        elif line.type == GmiLineType.HEADING2:
            yield f"## {line.text}"

        elif line.type == GmiLineType.HEADING3:
            yield f"### {line.text}"

        elif line.type == GmiLineType.LIST_ITEM:
            yield f"* {line.text}"

        elif line.type == GmiLineType.QUOTE:
            yield f"> {line.text}"

        elif line.type == GmiLineType.PREFORMAT_START:
            yield f"```{line.extra}"

        elif line.type == GmiLineType.PREFORMAT_LINE:
            yield line.text

        elif line.type == GmiLineType.PREFORMAT_END:
            yield "```"

        else:
            raise RuntimeWarning(f"Line type {line.type} not recognised.")


def reformat_file(output_format: str, input_path: Path, output_path: Path):

    # read input file
    document = GmiDocument()
    with open(input_path) as i:
        for line in i.readlines():
            document.append(line)

    # write trimmed gemtext
    if output_format == "GMI":
        with open(output_path, "w") as o:
            for line in document.emit_trim_gmi():
                o.write(line + "\n")

    # write naive HTML
    elif output_format == "HTML":
        with open(output_path, "w") as o:
            for line in emit_naive_html(document):
                o.write(line + "\n")

    # write naive HTML
    elif output_format == "MD":
        with open(output_path, "w") as o:
            for line in emit_commonmark(document):
                o.write(line + "\n")

    # alert on error
    else:
        raise RuntimeWarning("Output format not recognised.")
