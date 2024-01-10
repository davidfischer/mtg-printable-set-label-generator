import io
import logging
import os
from datetime import datetime
from itertools import cycle
from pathlib import Path

import requests
from cairosvg import svg2png
from config import defaults, pdf_templates
from config.utils import setup_args, setup_logger
from fpdf import FPDF, FlexTemplate
from PIL import Image, ImageOps

BASE_DIR = Path(os.path.abspath(os.path.dirname(__file__)))


class SetDividers:
    def __init__(self, paper_size, output_dir):
        self.paper_size = paper_size

        self.set_codes = []
        self.ignored_sets = defaults.IGNORED_SETS
        self.set_types = defaults.SET_TYPES
        self.minimum_set_size = defaults.MINIMUM_SET_SIZE

        self.output_dir = Path(output_dir)
        self.output_name = datetime.now().strftime("%Y-%M-%d") + "-set_dividers.pdf"

    def new_page_check(self, pdf, label_count):
        if label_count > 0 and label_count % defaults.LABELS_PER_PAGE == 0:
            logging.debug("Adding new page")
            pdf.add_page()

        label_count += 1
        return label_count


    def process_svg(self, svg_icon, set_icon_filename, target_size):
        logging.debug(f"svg_icon Type: {type(svg_icon)}")
        logging.debug(f"set_icon_filename Type: {type(set_icon_filename)}")

        if isinstance(svg_icon, Path):
            logging.debug("Transforming svg from disk")
            png_bytes = svg2png(url=svg_icon.as_posix())
        elif isinstance(svg_icon, bytes):
            logging.debug("Transforming svg from bytestream")
            png_bytes = svg2png(bytestring=svg_icon)

        logging.debug(f"png_bytes Type: {type(png_bytes)}")

        image = Image.open(io.BytesIO(png_bytes))

        ImageOps.pad(image, target_size).save(set_icon_filename.as_posix())

        return set_icon_filename

    def generate_dividers(self, sets=None):
        if sets:
            self.ignored_sets = ()
            self.minimum_set_size = 0
            self.set_types = ()
            self.set_codes = [exp.lower() for exp in sets]

        pdf = FPDF(orientation="landscape", format=self.paper_size)
        logging.debug("Creating initial page")
        pdf.add_page()

        if args.pips:
            template = FlexTemplate(pdf, pdf_templates.label_elements)
        else:
            template = FlexTemplate(pdf, pdf_templates.label_elements_no_pips)

        set_data = self.format_set_data()

        label_count = 0

        for mtg_set in set_data:
            logging.debug(f"Writing Label {label_count}")
            label_count = self.new_page_check(pdf, label_count)

            template["text_line_1"] = mtg_set["set_name"]
            template["text_line_2"] = f"{mtg_set["set_code"]} - {mtg_set["set_date"]}"
            template["set_icon"] = mtg_set["set_icon"]
            if args.pips:
                template["pip_icon"] = mtg_set["pip_icon"]

            template.render(offsetx=mtg_set["x_offset"], offsety=mtg_set["y_offset"])

        pdf.output(self.output_dir / self.output_name)


    def get_pips(self):
        """return an dict of pips and their base64 encoded svg from the resources/pips directory"""

        pips = list(Path(BASE_DIR / "resources" / "pips").glob("*.svg"))

        logging.debug(f"Colour pips found: {pips}")

        return pips

    def calculate_template_offsets(self):
        template_offsets = [
            {
                "x_offset": col * defaults.DIVIDER_WIDTH + defaults.PAGE_OFFSET,
                "y_offset": row * defaults.DIVIDER_HEIGHT + defaults.PAGE_OFFSET,
            }
            for row in range(defaults.LABELS_PER_COLUMN)
            for col in range(defaults.LABELS_PER_ROW)
        ]

        logging.debug(f"Template offset values: {template_offsets}")

        return template_offsets

    def get_set_data(self):
        logging.info("Getting set data and icons from Scryfall")

        # https://scryfall.com/docs/api/sets
        # https://scryfall.com/docs/api/sets/all
        resp = requests.get("https://api.scryfall.com/sets")
        resp.raise_for_status()

        scryfall_response = resp.json()["data"]
        scryfall_set_data = []
        for mtg_set in scryfall_response:
            if mtg_set["code"] in self.ignored_sets:
                continue
            elif mtg_set["card_count"] < self.minimum_set_size:
                continue
            elif self.set_types and mtg_set["set_type"] not in self.set_types:
                continue
            elif self.set_codes and mtg_set["code"].lower() not in self.set_codes:
                # Scryfall set codes are always lowercase
                continue
            else:
                scryfall_set_data.append(mtg_set)

        # Warn on any unknown set codes
        if self.set_codes:
            known_sets = set([mtg_set["code"] for mtg_set in scryfall_response])
            specified_sets = set([code.lower() for code in self.set_codes])
            unknown_sets = specified_sets.difference(known_sets)
            for set_code in unknown_sets:
                logging.warning(f"Unknown MTG set: {set_code}")

        scryfall_set_data.reverse()
        logging.debug(f"Set data: {scryfall_set_data}")
        return scryfall_set_data

    def get_set_icon(self, scryfall_id, scryfall_icon_svg_uri):
        """
        Returns the path to the set icon, downloading it if necessary
        """

        set_icons_path = Path(
            BASE_DIR / "resources" / "set_icons"
        )
        set_icon_filename = set_icons_path / f"{scryfall_id}.png"

        # Check if the icon already exists
        if set_icon_filename.is_file():
            logging.debug(f"Set icon found: {set_icon_filename}")
            return set_icon_filename
        else:
            logging.debug(f"Downloading set icon: {scryfall_icon_svg_uri}")
            resp = requests.get(scryfall_icon_svg_uri)
            resp.raise_for_status()

            set_icon_svg = resp.content

            processed_icon = self.process_svg(
                set_icon_svg,
                set_icon_filename,
                target_size=(256, 256),
            )

            if processed_icon.is_file():
                logging.debug(f"Set icon downloaded: {set_icon_filename}")
                return processed_icon

    def format_set_data(self):
        """
        Create the label data for the sets
        """

        # Get set data from scryfall
        set_data = self.get_set_data()
        template_offsets_cycle = cycle(self.calculate_template_offsets())

        if args.pips:
            logging.debug("Generating set data with colour pips")
            colour_pips = self.get_pips()

            formatted_set_data = [
                {
                    "set_name": defaults.RENAME_SETS.get(mtg_set["name"], mtg_set["name"]),
                    "set_id": mtg_set["id"],
                    "set_code": mtg_set["code"].upper(),
                    "set_date": datetime.strptime(
                        mtg_set["released_at"], "%Y-%m-%d"
                    ).strftime("%b %Y"),
                    "set_icon": self.get_set_icon(mtg_set["id"], mtg_set["icon_svg_uri"]),
                    "pip_icon": pip,
                    **next(template_offsets_cycle),
                }
                for mtg_set in set_data
                for pip in colour_pips
            ]
            logging.debug(f"Formatted set data with pips: {formatted_set_data}")

        else:
            logging.debug("Generating set data without colour pips")

            formatted_set_data = [
                {
                    "set_name": defaults.RENAME_SETS.get(
                        mtg_set["name"], mtg_set["name"]
                    ),
                    "set_id": mtg_set["id"],
                    "set_code": mtg_set["code"].upper(),
                    "set_date": datetime.strptime(
                        mtg_set["released_at"], "%Y-%m-%d"
                    ).strftime("%b %Y"),
                    "set_icon": self.get_set_icon(
                        mtg_set["id"], mtg_set["icon_svg_uri"]
                    ),
                    **next(template_offsets_cycle),
                }
                for mtg_set in set_data
            ]
            logging.debug(f"Formatted set data: {formatted_set_data}")

        return formatted_set_data


def main():
    generator = SetDividers(args.paper_size, args.output_dir)
    generator.generate_dividers(args.sets)


if __name__ == "__main__":
    args = setup_args()
    debug = args.debug if args.debug else False
    setup_logger(debug)

    main()
