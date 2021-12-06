#!/usr/bin/env python3
import argparse
import contextlib
import logging
import re
import sys
from contextlib import redirect_stdout
# namedtuple with default arguments
# <https://stackoverflow.com/a/18348004/353337>
from dataclasses import dataclass
from io import StringIO
from os import error
from pathlib import Path
from typing import Optional, Union

from pytest import Pytester


@dataclass
class CodeBlock:
    code: str
    lineno: int
    syntax: Optional[str] = None
    expected_output: Optional[str] = None
    expect_exception: bool = False


def extract_from_file(f: Union[str, bytes, Path],
                      encoding: Optional[str] = None,
                      *args,
                      **kwargs):
    with open(f, "r", encoding=encoding) as handle:
        return extract_from_buffer(handle, *args, **kwargs)


def extract_from_buffer(f, max_num_lines: int = 10000):
    out = "#!/usr/bin/env python3\n"
    previous_line = None
    k = 1

    while True:
        line = f.readline()
        k += 1
        if not line:
            # EOF
            break
        matches = re.match("([>\s]*|\s*)[~]{3}", line.lstrip())
        if matches:
            # Indent can either be a number of spaces,
            # or a greater than follow by a space a number of times
            leading_indent = re.match("([>\s]*|\s*)", line)
            lineno = k - 1
            # read the block
            code_block = []
            while True:
                line = f.readline()
                k += 1
                if not line:
                    raise RuntimeError(
                        "Hit end-of-file prematurely. Syntax error?")
                if k > max_num_lines:
                    raise RuntimeError(
                        f"File too large (> {max_num_lines} lines). Set max_num_lines."
                    )
                # check if end of block
                if re.match("([>\s]*|\s*)[~]{3}", line.lstrip()):
                    break
                # Cut leading indents
                line = line[leading_indent.span()[1]:]
                code_block.append(line)

            line = f.readline()
            if not line:
                raise RuntimeError(
                    f"Hit end-of-file prematurely at line: {lineno}. Syntax error?"
                )

            if re.match("[>\s]*\{:\s*\.language-python\}", line.lstrip()):
                if previous_line is None:
                    out += "".join(code_block)
                    continue

                # check for keywords
                m = re.search("<!--cce:(.*)-->", previous_line.strip())
                if m is None:
                    out += "".join(code_block)
                    continue

                keyword = m.group(1)

                # handle special tags
                if keyword == "skip":
                    continue
                else:
                    raise RuntimeError(
                        'Unknown pytest-codeblocks keyword "{keyword}."')

        previous_line = line
    return out


parser = argparse.ArgumentParser(
    description='Extract code  blocks from carpentries markdown.')
parser.add_argument('-f',
                    '--file',
                    help='The file to extract from',
                    required=True)
parser.add_argument('-o',
                    '--output_code',
                    help='Whether to write the code content to stdout',
                    action='store_true')
args = parser.parse_args()

contents = extract_from_file(args.file)
if args.output_code:
    print(contents)

errors = 0
f = StringIO()
with redirect_stdout(f):
    try:
        exec(contents)
    except Exception as e:
        logging.error("Exception occurred while trying to run code:")
        logging.error(e, exc_info=True)
        logging.error("Code: ")
        logging.error(contents)
        errors = errors + 1
s = f.getvalue()
if errors > 0:
    logging.error(s)
    sys.exit(errors)
elif args.output_code:
    print(contents)
