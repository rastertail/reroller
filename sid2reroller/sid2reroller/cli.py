"""
Command-line frontend
"""

import argparse

from sid2reroller.convert import convert


def main():
    """
    Command-line entry point
    """

    parser = argparse.ArgumentParser(
        description="Converter from PSID songs to Reroller input streams"
    )
    parser.add_argument("input", type=argparse.FileType("rb"), help="Input PSID file")
    parser.add_argument(
        "-o",
        "--out",
        type=argparse.FileType("wb"),
        default="out.rr",
        help="Output file",
    )
    parser.add_argument(
        "-f", "--frames", type=int, default=10000, help="Number of frames to render"
    )
    args = parser.parse_args()

    args.out.write(convert(args.input.read(), args.frames))
