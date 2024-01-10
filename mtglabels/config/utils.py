import argparse
import logging

from config import defaults


def setup_args():
    parser = argparse.ArgumentParser(description="Generate MTG labels")
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging level",
    )
    parser.add_argument(
        "--output-dir",
        default=defaults.DEFAULT_OUTPUT_DIR,
        help="Output labels to this directory",
    )
    parser.add_argument(
        "--paper-size",
        default=defaults.DEFAULT_PAPER_SIZE,
        choices=defaults.PAPER_SIZES.keys(),
        help='Use this paper size (default: "A4")',
        type=str.lower,
    )
    parser.add_argument(
        "--sets",
        nargs="*",
        help=(
            "Only output sets with the specified set code (eg. MH1, NEO). "
            "This can be used multiple times."
        ),
        metavar="SET",
    )
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
