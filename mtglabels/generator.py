import base64
import logging
import os
from datetime import datetime
from pathlib import Path

import cairosvg
import jinja2
import requests
from config import defaults
from config.utils import setup_args, setup_logger

BASE_DIR = Path(os.path.abspath(os.path.dirname(__file__)))

ENV = jinja2.Environment(
    loader=jinja2.FileSystemLoader(BASE_DIR / "templates"),
    autoescape=jinja2.select_autoescape(["html", "xml"]),
)


class LabelGenerator:
    COLS = 4
    ROWS = 15
    MARGIN = 200  # in 1/10 mm
    START_X = MARGIN
    START_Y = MARGIN

    def __init__(self, paper_size, output_dir):
        self.paper_size = paper_size
        paper = defaults.PAPER_SIZES[paper_size]

        self.set_codes = []
        self.ignored_sets = defaults.IGNORED_SETS
        self.set_types = defaults.SET_TYPES
        self.minimum_set_size = defaults.MINIMUM_SET_SIZE

        self.width = paper["width"]
        self.height = paper["height"]

        # These are the deltas between rows and columns
        self.delta_x = (self.width - (2 * self.MARGIN)) / self.COLS
        self.delta_y = (self.height - (2 * self.MARGIN)) / self.ROWS

        self.output_dir = Path(output_dir)

    def generate_labels(self, sets=None):
        if sets:
            self.ignored_sets = ()
            self.minimum_set_size = 0
            self.set_types = ()
            self.set_codes = [exp.lower() for exp in sets]

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
            outfile_svg = self.output_dir / f"labels-{self.paper_size}-{page:02}.svg"
            outfile_pdf = str(
                self.output_dir / f"labels-{self.paper_size}-{page:02}.pdf"
            )

            logging.info(f"Writing {outfile_svg}...")
            with open(outfile_svg, "w") as fd:
                fd.write(output)

            logging.info(f"Writing {outfile_pdf}...")
            with open(outfile_svg, "rb") as fd:
                cairosvg.svg2pdf(
                    file_obj=fd,
                    write_to=outfile_pdf,
                )

            page += 1

    def get_set_data(self):
        logging.info("Getting set data and icons from Scryfall")

        # https://scryfall.com/docs/api/sets
        # https://scryfall.com/docs/api/sets/all
        resp = requests.get("https://api.scryfall.com/sets")
        resp.raise_for_status()

        data = resp.json()["data"]
        set_data = []
        for exp in data:
            if exp["code"] in self.ignored_sets:
                continue
            elif exp["card_count"] < self.minimum_set_size:
                continue
            elif self.set_types and exp["set_type"] not in self.set_types:
                continue
            elif self.set_codes and exp["code"].lower() not in self.set_codes:
                # Scryfall set codes are always lowercase
                continue
            else:
                set_data.append(exp)

        # Warn on any unknown set codes
        if self.set_codes:
            known_sets = set([exp["code"] for exp in data])
            specified_sets = set([code.lower() for code in self.set_codes])
            unknown_sets = specified_sets.difference(known_sets)
            for set_code in unknown_sets:
                logging.warning("Unknown set '%s'", set_code)

        set_data.reverse()
        return set_data

    def create_set_label_data(self):
        """
        Create the label data for the sets

        This handles positioning of the label's (x, y) coords
        """
        labels = []
        x = self.START_X
        y = self.START_Y

        # Get set data from scryfall
        set_data = self.get_set_data()

        for exp in set_data:
            name = defaults.RENAME_SETS.get(exp["name"], exp["name"])
            icon_resp = requests.get(exp["icon_svg_uri"])
            icon_b64 = None
            colour_indicator = None

            colour_indicator_path = Path(BASE_DIR / "templates" / "r.svg")
            logging.info(
                f"Checking for colour indicator file at: {colour_indicator_path}"
            )

            # if colour_indicator_path.exists():
            #     logging.info(
            #         f"Colour indicator file exists: {colour_indicator_path.exists()}"
            #     )
            #     # colour_indicator =  colour_indicator_path.name
            #     colour_indicator = base64.b64encode(
            #         colour_indicator_path.read_bytes()
            #     ).decode("utf-8")
            if icon_resp.ok:
                icon_b64 = base64.b64encode(icon_resp.content).decode("utf-8")

            labels.append(
                {
                    "name": name,
                    "code": exp["code"],
                    "date": datetime.strptime(exp["released_at"], "%Y-%m-%d").date(),
                    "icon_url": exp["icon_svg_uri"],
                    "icon_b64": icon_b64,
                    "colour_indicator": colour_indicator,
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


def main():
    generator = LabelGenerator(args.paper_size, args.output_dir)
    generator.generate_labels(args.sets)


if __name__ == "__main__":
    args = setup_args()
    debug = args.debug if args.debug else False
    setup_logger(debug)

    main()
