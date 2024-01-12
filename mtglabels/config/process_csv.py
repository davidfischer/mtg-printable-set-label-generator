import logging
from ast import literal_eval
from pathlib import Path

import pandas as pd

from mtglabels.config.utils import setup_args, setup_logger


def extract_colors(color_str):
    if isinstance(color_str, str):
        # Safely evaluate the string using literal_eval
        try:
            return set(literal_eval(color_str))
        except (ValueError, SyntaxError):
            # Handle the case where the string is not a valid list
            return set()
    else:
        # Handle the case where the entry is not a string
        return set()


def process_csv(CSV_FILE):
    df = pd.read_csv(CSV_FILE)
    df.columns = df.columns.str.strip()

    # Use a dictionary comprehension to reformat the data
    result = {
        set_code: {
            "Colors": list(
                set(
                    color
                    for colors_str in df[df["Set Code"] == set_code]["Color"]
                    for color_set in extract_colors(colors_str)
                    for color in color_set
                )
            ),
            "Count": int(
                (
                    df[df["Set Code"] == set_code]["Number of Non-foil"]
                    + df[df["Set Code"] == set_code]["Number of Foil"]
                ).sum()
            ),
        }
        for set_code in df["Set Code"].unique()
    }

    large_sets = [set for set in result if result[set]["Count"] > 50]
    small_sets = [set for set in result if result[set]["Count"] <= 50]

    logging.debug(f"Large Sets: {large_sets}")
    logging.debug(f"Small Sets: {small_sets}")

    mtg_sets = {
        "large": large_sets,
        "small": small_sets,
    }

    return mtg_sets


def main(CSV_FILE):
    mtg_sets = process_csv(CSV_FILE)

    logging.debug(f"MTG Sets: {mtg_sets}")


if __name__ == "__main__":
    args = setup_args()
    debug = args.debug if args.debug else False
    setup_logger(debug)

    CSV_FILE = Path("mtglabels/tmp/test.csv")

    main(CSV_FILE)
