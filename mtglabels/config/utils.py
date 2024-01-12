import argparse
import logging

from mtglabels.config import defaults


def setup_args():
    parser = argparse.ArgumentParser(description="Generate MTG labels")
    parser.add_argument(
        "--debug",
        "-d",
        default=False,
        action="store_true",
        help="Enable debug logging when running script",
    )
    parser.add_argument(
        "--output-dir",
        "-o",
        default=defaults.DEFAULT_OUTPUT_DIR,
        help="Output labels to this directory",
    )
    parser.add_argument(
        "--paper-size",
        "-p",
        default=defaults.DEFAULT_PAPER_SIZE,
        choices=defaults.PAPER_SIZES.keys(),
        help='Use this paper size (default: "A4")',
        type=str.lower,
    )
    parser.add_argument(
        "--disable-offset",
        action="store_true",
        default=False,
        help="If used, labels will not be centered on the page and begin at the top left corner of the page (default: False)",
    )
    parser.add_argument(
        "--sets",
        "-s",
        nargs="*",
        help=(
            "Only output sets with the specified set code (eg. MH1, NEO). "
            "This can be used multiple times."
        ),
        metavar="SET_CODE",
    )
    parser.add_argument(
        "--csv",
        help="Captures set information from a CSV file",
        metavar="CSV_PATH",
        type=argparse.FileType("r"),
    ),
    parser.add_argument(
        "--pips",
        action="store_true",
        help="Optionally outputs one label per colour pips for each set (Multi-colour, Colourless, WUBRG)",
    )

    return parser.parse_args()


def setup_logger(debug=False):
    log_level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(filename)s - %(funcName)s - %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
