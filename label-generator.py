import argparse
import os
import subprocess
from datetime import datetime

import jinja2
import requests


BASE_DIR = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))

ENV = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(BASE_DIR, "templates")),
    autoescape=jinja2.select_autoescape(["html", "xml"]),
)

# Set types we are interested in
SET_TYPES = (
    "core",
    "expansion",
    "starter",  # Portal, P3k, welcome decks
    "masters",
    "commander",
    "planechase",
    "draft_innovation",  # Battlebond, Conspiracy
    "duel_deck",  # Duel Deck Elves,
    "premium_deck",  # Premium Deck Series: Slivers, Premium Deck Series: Graveborn
    "from_the_vault",  # Make sure to adjust the MINIMUM_SET_SIZE if you want these
    "archenemy",
    "box",
    "funny",  # Unglued, Unhinged, Ponies: TG, etc.
    # "memorabilia",  # Commander's Arsenal, Celebration Cards, World Champ Decks
    # "spellbook",
    # These are relatively large groups of sets
    # You almost certainly don't want these
    # "token",
    # "promo",
)

# Only include sets at least this size
# For reference, the smallest proper expansion is Arabian Nights with 78 cards
MINIMUM_SET_SIZE = 50

# Set codes you might want to ignore
IGNORED_SETS = (
    "cmb1",  # Mystery Booster Playtest Cards
    "amh1",  # Modern Horizon Art Series
    "cmb2",  # Mystery Booster Playtest Cards Part Deux
)

# Used to rename very long set names
RENAME_SETS = {
    "Fourth Edition Foreign Black Border": "Fourth Edition FBB",
    "Introductory Two-Player Set": "Intro Two-Player Set",
    "Commander Anthology Volume II": "Commander Anthology II",
    "Planechase Anthology Planes": "Planechase Anth. Planes",
    "Mystery Booster Playtest Cards": "Mystery Booster Playtest",
    "World Championship Decks 1997": "World Championship 1997",
    "World Championship Decks 1998": "World Championship 1998",
    "World Championship Decks 1999": "World Championship 1999",
    "World Championship Decks 2000": "World Championship 2000",
    "World Championship Decks 2001": "World Championship 2001",
    "World Championship Decks 2002": "World Championship 2002",
    "World Championship Decks 2003": "World Championship 2003",
    "World Championship Decks 2004": "World Championship 2004",
    "Duel Decks: Elves vs. Goblins": "DD: Elves vs. Goblins",
    "Duel Decks: Jace vs. Chandra": "DD: Jace vs. Chandra",
    "Duel Decks: Divine vs. Demonic": "DD: Divine vs. Demonic",
    "Duel Decks: Garruk vs. Liliana": "DD: Garruk vs. Liliana",
    "Duel Decks: Phyrexia vs. the Coalition": "DD: Phyrexia vs. Coalition",
    "Duel Decks: Elspeth vs. Tezzeret": "DD: Elspeth vs. Tezzeret",
    "Duel Decks: Knights vs. Dragons": "DD: Knights vs. Dragons",
    "Duel Decks: Ajani vs. Nicol Bolas": "DD: Ajani vs. Nicol Bolas",
    "Duel Decks: Heroes vs. Monsters": "DD: Heroes vs. Monsters",
    "Duel Decks: Speed vs. Cunning": "DD: Speed vs. Cunning",
    "Duel Decks Anthology: Elves vs. Goblins": "DDA: Elves vs. Goblins",
    "Duel Decks Anthology: Jace vs. Chandra": "DDA: Jace vs. Chandra",
    "Duel Decks Anthology: Divine vs. Demonic": "DDA: Divine vs. Demonic",
    "Duel Decks Anthology: Garruk vs. Liliana": "DDA: Garruk vs. Liliana",
    "Duel Decks: Elspeth vs. Kiora": "DD: Elspeth vs. Kiora",
    "Duel Decks: Zendikar vs. Eldrazi": "DD: Zendikar vs. Eldrazi",
    "Duel Decks: Blessed vs. Cursed": "DD: Blessed vs. Cursed",
    "Duel Decks: Nissa vs. Ob Nixilis": "DD: Nissa vs. Ob Nixilis",
    "Duel Decks: Merfolk vs. Goblins": "DD: Merfolk vs. Goblins",
    "Duel Decks: Elves vs. Inventors": "DD: Elves vs. Inventors",
    "Premium Deck Series: Slivers": "Premium Deck Slivers",
    "Premium Deck Series: Graveborn": "Premium Deck Graveborn",
    "Premium Deck Series: Fire and Lightning": "Premium Deck Fire & Lightning",
    "Mystery Booster Retail Edition Foils": "Mystery Booster Retail Foils",
    "Adventures in the Forgotten Realms": "Forgotten Realms",
}


class LabelGenerator:

    DEFAULT_OUTPUT_DIR = os.path.join(BASE_DIR, "output")

    COLS = 4
    ROWS = 15
    MARGIN = 200  # in 1/10 mm
    START_X = MARGIN
    START_Y = MARGIN

    PAPER_SIZES = {
        "letter": {"width": 2790, "height": 2160,},  # in 1/10 mm
        "a4": {"width": 2970, "height": 2100,},
    }
    DEFAULT_PAPER_SIZE = "letter"

    def __init__(self, paper_size=None, output_dir=None):
        self.paper_size = paper_size or DEFAULT_PAPER_SIZE
        paper = self.PAPER_SIZES[paper_size]

        self.width = paper["width"]
        self.height = paper["height"]

        # These are the deltas between rows and columns
        self.delta_x = (self.width - (2 * self.MARGIN)) / self.COLS
        self.delta_y = (self.height - (2 * self.MARGIN)) / self.ROWS

        self.output_dir = output_dir or DEFAULT_OUTPUT_DIR

        # Set data from scryfall
        self.set_data = self.get_set_data()

    def generate_labels(self):
        page = 1
        labels = self.create_set_label_data()
        while labels:
            exps = []
            while labels and len(exps) < (self.ROWS * self.COLS):
                exps.append(labels.pop(0))

            # Render the label template
            template = ENV.get_template("labels.svg")
            output = template.render(
                labels=exps,
                horizontal_guides=self.create_horizontal_cutting_guides(),
                vertical_guides=self.create_vertical_cutting_guides(),
                WIDTH=self.width,
                HEIGHT=self.height,
            )
            outfile = os.path.join(
                self.output_dir, f"labels-{self.paper_size}-{page:02}.svg"
            )
            print(f"Writing {outfile}...")
            with open(outfile, "w") as fd:
                fd.write(output)

            page += 1

    def get_set_data(self):
        print("Getting set data and icons from Scryfall")

        # https://scryfall.com/docs/api/sets
        # https://scryfall.com/docs/api/sets/all
        resp = requests.get("https://api.scryfall.com/sets")
        resp.raise_for_status()

        data = resp.json()["data"]
        data = [
            exp
            for exp in data
            if exp["set_type"] in SET_TYPES
            and not exp["digital"]
            and exp["code"] not in IGNORED_SETS
            and exp["card_count"] >= MINIMUM_SET_SIZE
        ]
        data.reverse()

        return data

    def create_set_label_data(self):
        """
        Create the label data for the sets

        This handles positioning of the label's (x, y) coords
        """
        labels = []
        x = self.START_X
        y = self.START_Y
        for exp in self.set_data:
            name = RENAME_SETS.get(exp["name"], exp["name"])
            labels.append(
                {
                    "name": name,
                    "code": exp["code"],
                    "date": datetime.strptime(exp["released_at"], "%Y-%m-%d").date(),
                    "icon_url": exp["icon_svg_uri"],
                    "x": x,
                    "y": y,
                }
            )

            y += self.delta_y

            # Start a new column if needed
            if len(labels) % self.ROWS == 0:
                x += self.delta_x
                y = self.START_Y

            # Start a new page if needed
            if len(labels) % (self.ROWS * self.COLS) == 0:
                x = self.START_X
                y = self.START_Y

        return labels

    def create_horizontal_cutting_guides(self):
        """Create horizontal cutting guides to help cut the labels out straight"""
        horizontal_guides = []
        for i in range(self.ROWS + 1):
            horizontal_guides.append(
                {
                    "x1": self.MARGIN / 2,
                    "x2": self.MARGIN * 0.8,
                    "y1": self.MARGIN + i * self.delta_y,
                    "y2": self.MARGIN + i * self.delta_y,
                }
            )
            horizontal_guides.append(
                {
                    "x1": self.width - self.MARGIN / 2,
                    "x2": self.width - self.MARGIN * 0.8,
                    "y1": self.MARGIN + i * self.delta_y,
                    "y2": self.MARGIN + i * self.delta_y,
                }
            )

        return horizontal_guides

    def create_vertical_cutting_guides(self):
        """Create horizontal cutting guides to help cut the labels out straight"""
        vertical_guides = []
        for i in range(self.COLS + 1):
            vertical_guides.append(
                {
                    "x1": self.MARGIN + i * self.delta_x,
                    "x2": self.MARGIN + i * self.delta_x,
                    "y1": self.MARGIN / 2,
                    "y2": self.MARGIN * 0.8,
                }
            )
            vertical_guides.append(
                {
                    "x1": self.MARGIN + i * self.delta_x,
                    "x2": self.MARGIN + i * self.delta_x,
                    "y1": self.height - self.MARGIN / 2,
                    "y2": self.height - self.MARGIN * 0.8,
                }
            )

        return vertical_guides


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate MTG labels")

    parser.add_argument(
        "--output-dir",
        default=LabelGenerator.DEFAULT_OUTPUT_DIR,
        help='Output labels to this directory',
    )
    parser.add_argument(
        "--paper-size",
        default=LabelGenerator.DEFAULT_PAPER_SIZE,
        choices=LabelGenerator.PAPER_SIZES.keys(),
        help='Use this paper size (default: "letter")',
    )

    args = parser.parse_args()

    generator = LabelGenerator(args.paper_size, args.output_dir)
    generator.generate_labels()
