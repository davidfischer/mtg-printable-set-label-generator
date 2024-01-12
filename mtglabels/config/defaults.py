import os
from pathlib import Path

API_ENDPOINT = "https://api.scryfall.com/sets"
DEFAULT_OUTPUT_DIR = Path(os.getcwd()) / "output"

# MTG Card Size: 63mm x 88mm
# Label Size: 65mm x 95mm
DIVIDER_WIDTH = 65
DIVIDER_HEIGHT = 95

# Page Layout Settings
LABELS_PER_ROW = 4
LABELS_PER_COLUMN = 2
LABELS_PER_PAGE = LABELS_PER_ROW * LABELS_PER_COLUMN

DEFAULT_PAPER_SIZE = "A4"
PAPER_SIZES = {
    "letter": {
        "width": 279,
        "height": 216,
    },
    "a4": {
        "width": 297,
        "height": 210,
    },
}


# Only include sets at least this size
# For reference, the smallest proper expansion is Arabian Nights with 78 cards
MINIMUM_SET_SIZE = 50

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

# Set codes you might want to ignore
IGNORED_SETS = (
    "cmb1",  # Mystery Booster Playtest Cards
    "amh1",  # Modern Horizon Art Series
    "cmb2",  # Mystery Booster Playtest Cards Part Deux
    "fbb",  # Foreign Black Border
    "sum",  # Summer Magic / Edgar
    "4bb",  # Fourth Edition Foreign Black Border
    "bchr",  # Chronicles Foreign Black Border
    "rin",  # Rinascimento
    "ren",  # Renaissance
    "rqs",  # Rivals Quick Start Set
    "itp",  # Introductory Two-Player Set
    "sir",  # Shadows over Innistrad Remastered
    "sis",  # Shadows of the Past
    "cst",  # Coldsnap Theme Decks
)

# Used to rename very long set names
RENAME_SETS = {
    "Adventures in the Forgotten Realms Minigames": "Forgotten Realms Minigames",
    "Adventures in the Forgotten Realms": "Forgotten Realms",
    "Angels: They're Just Like Us but Cooler and with Wings": "Angels: Just Like Us",
    "Archenemy: Nicol Bolas Schemes": "Archenemy: Bolas Schemes",
    "Chronicles Foreign Black Border": "Chronicles FBB",
    "Commander Anthology Volume II": "Commander Anthology II",
    "Commander Legends: Battle for Baldur's Gate": "CMDR: Baldur's Gate",
    "Crimson Vow Commander": "CMDR: Crimson Vow",
    "Dominaria United Commander": "CMDR Dominaria United",
    "Duel Decks Anthology: Divine vs. Demonic": "DDA: Divine vs. Demonic",
    "Duel Decks Anthology: Elves vs. Goblins": "DDA: Elves vs. Goblins",
    "Duel Decks Anthology: Garruk vs. Liliana": "DDA: Garruk vs. Liliana",
    "Duel Decks Anthology: Jace vs. Chandra": "DDA: Jace vs. Chandra",
    "Duel Decks: Ajani vs. Nicol Bolas": "DD: Ajani vs. Nicol Bolas",
    "Duel Decks: Blessed vs. Cursed": "DD: Blessed vs. Cursed",
    "Duel Decks: Divine vs. Demonic": "DD: Divine vs. Demonic",
    "Duel Decks: Elspeth vs. Kiora": "DD: Elspeth vs. Kiora",
    "Duel Decks: Elspeth vs. Tezzeret": "DD: Elspeth vs. Tezzeret",
    "Duel Decks: Elves vs. Goblins": "DD: Elves vs. Goblins",
    "Duel Decks: Elves vs. Inventors": "DD: Elves vs. Inventors",
    "Duel Decks: Garruk vs. Liliana": "DD: Garruk vs. Liliana",
    "Duel Decks: Heroes vs. Monsters": "DD: Heroes vs. Monsters",
    "Duel Decks: Izzet vs. Golgari": "DD: Izzet vs. Golgari",
    "Duel Decks: Jace vs. Chandra": "DD: Jace vs. Chandra",
    "Duel Decks: Knights vs. Dragons": "DD: Knights vs. Dragons",
    "Duel Decks: Merfolk vs. Goblins": "DD: Merfolk vs. Goblins",
    "Duel Decks: Mirrodin Pure vs. New Phyrexia": "DD: Mirrodin vs.N Phyrexia",
    "Duel Decks: Nissa vs. Ob Nixilis": "DD: Nissa vs. Ob Nixilis",
    "Duel Decks: Phyrexia vs. the Coalition": "DD: Phyrexia vs. Coalition",
    "Duel Decks: Speed vs. Cunning": "DD: Speed vs. Cunning",
    "Duel Decks: Zendikar vs. Eldrazi": "DD: Zendikar vs. Eldrazi",
    "Forgotten Realms Commander": "CMDR: Forgotten Realms",
    "Fourth Edition Foreign Black Border": "Fourth Edition FBB",
    "Global Series Jiang Yanggu & Mu Yanling": "Jiang Yanggu & Mu Yanling",
    "Innistrad: Crimson Vow Minigames": "Crimson Vow Minigames",
    "Introductory Two-Player Set": "Intro Two-Player Set",
    "Kaldheim Commander": "CMDR: Kaldheim",
    "March of the Machine Commander": "CMDR: March of the Machine",
    "March of the Machine: The Aftermath": "MOM: Aftermath",
    "Midnight Hunt Commander": "CMDR: Midnight Hunt",
    "Mystery Booster Playtest Cards 2019": "MB Playtest Cards 2019",
    "Mystery Booster Playtest Cards 2021": "MB Playtest Cards 2021",
    "Mystery Booster Playtest Cards": "Mystery Booster Playtest",
    "Mystery Booster Retail Edition Foils": "Mystery Booster Foils",
    "Neon Dynasty Commander": "CMDR: Neon Dynasty",
    "New Capenna Commander": "CMDR: New Capenna",
    "Phyrexia: All Will Be One Commander": "CMDR: Phyrexia",
    "Planechase Anthology Planes": "Planechase Anth. Planes",
    "Premium Deck Series: Fire and Lightning": "PD: Fire & Lightning",
    "Premium Deck Series: Graveborn": "Premium Deck Graveborn",
    "Premium Deck Series: Slivers": "Premium Deck Slivers",
    "Shadows over Innistrad Remastered": "SOI Remastered",
    "Starter Commander Decks": "CMDR: Starter Decks",
    "Strixhaven: School of Mages Minigames": "Strixhaven Minigames",
    "Tales of Middle-earth Commander": "CMDR: LOTR",
    "The Brothers' War Commander": "CMDR: Brothers' War",
    "The Brothers' War Retro Artifacts": "Brothers' War Retro",
    "The Lord of the Rings: Tales of Middle-earth": "LOTR: Tales of Middle-earth",
    "The Lost Caverns of Ixalan Commander": "CMDR: Lost Caverns Ixalan",
    "Warhammer 40,000 Commander": "CMDR: Warhammer 40K",
    "Wilds of Eldraine Commander": "CMDR: Wilds of Eldraine",
    "Wilds of Eldraine: Enchanting Tales": "WOE: Enchanting Tales",
    "World Championship Decks 1997": "World Championship 1997",
    "World Championship Decks 1998": "World Championship 1998",
    "World Championship Decks 1999": "World Championship 1999",
    "World Championship Decks 2000": "World Championship 2000",
    "World Championship Decks 2001": "World Championship 2001",
    "World Championship Decks 2002": "World Championship 2002",
    "World Championship Decks 2003": "World Championship 2003",
    "World Championship Decks 2004": "World Championship 2004",
    "Zendikar Rising Commander": "CMDR: Zendikar Rising",
}

# Regex to find string longer than 26 characters - ": ".{26,}"
