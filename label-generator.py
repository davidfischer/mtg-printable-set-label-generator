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
}

COLS = 4
ROWS = 15
WIDTH = 2790  # Width in 1/10 mm of US Letter paper
HEIGHT = 2160
MARGIN = 200
START_X = MARGIN
START_Y = MARGIN
DELTA_X = (WIDTH - (2 * MARGIN)) / COLS
DELTA_Y = (HEIGHT - (2 * MARGIN)) / ROWS


def get_set_data():
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


def create_set_label_data():
    """
    Create the label data for the sets

    This handles positioning of the label's (x, y) coords
    """
    labels = []
    x = START_X
    y = START_Y
    for exp in get_set_data():
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

        y += DELTA_Y

        # Start a new column if needed
        if len(labels) % ROWS == 0:
            x += DELTA_X
            y = START_Y

        # Start a new page if needed
        if len(labels) % (ROWS * COLS) == 0:
            x = START_X
            y = START_Y

    return labels


def create_horizontal_cutting_guides():
    """Create horizontal cutting guides to help cut the labels out straight"""
    horizontal_guides = []
    for i in range(ROWS + 1):
        horizontal_guides.append(
            {
                "x1": MARGIN / 2,
                "x2": MARGIN * 0.8,
                "y1": MARGIN + i * DELTA_Y,
                "y2": MARGIN + i * DELTA_Y,
            }
        )
        horizontal_guides.append(
            {
                "x1": WIDTH - MARGIN / 2,
                "x2": WIDTH - MARGIN * 0.8,
                "y1": MARGIN + i * DELTA_Y,
                "y2": MARGIN + i * DELTA_Y,
            }
        )

    return horizontal_guides


def create_vertical_cutting_guides():
    """Create horizontal cutting guides to help cut the labels out straight"""
    vertical_guides = []
    for i in range(COLS + 1):
        vertical_guides.append(
            {
                "x1": MARGIN + i * DELTA_X,
                "x2": MARGIN + i * DELTA_X,
                "y1": MARGIN / 2,
                "y2": MARGIN * 0.8,
            }
        )
        vertical_guides.append(
            {
                "x1": MARGIN + i * DELTA_X,
                "x2": MARGIN + i * DELTA_X,
                "y1": HEIGHT - MARGIN / 2,
                "y2": HEIGHT - MARGIN * 0.8,
            }
        )

    return vertical_guides


if __name__ == "__main__":
    page = 1
    labels = create_set_label_data()
    while labels:
        exps = []
        while labels and len(exps) < (ROWS * COLS):
            exps.append(labels.pop(0))

        # Render the label template
        template = ENV.get_template("labels.svg")
        output = template.render(
            labels=exps,
            horizontal_guides=create_horizontal_cutting_guides(),
            vertical_guides=create_vertical_cutting_guides(),
            WIDTH=WIDTH,
            HEIGHT=HEIGHT,
        )
        outfile = os.path.join(BASE_DIR, "output", f"labels{page:02}.svg")
        print(f"Writing {outfile}...")
        with open(outfile, "w") as fd:
            fd.write(output)

        page += 1
