from itertools import cycle

from config.pdf_templates import divider_height, divider_width, label_elements
from fpdf import FPDF, FlexTemplate

# Page Settings
page_offset = 5
labels_per_row = 4
labels_per_column = 2
labels_per_page = labels_per_row * labels_per_column


def new_page_check(label_count):
    if label_count > 0 and label_count % labels_per_page == 0:
        pdf.add_page()

    print(f"Label count: {label_count}")
    return label_count


pdf = FPDF(orientation="landscape", format="A4")
pdf.add_page()
template = FlexTemplate(pdf, label_elements)

# text_line_1 max length is 27 characters

card_divider_data = [
    {
        "text_line_1": "LOTR: Tales of Middle Earth",
        "text_line_2": "LTR - June 2023",
        "set_icon": "mtglabels/templates/pips/multi.svg",
        "colour_icon": "mtglabels/templates/pips/r.svg",
    },
    {
        "text_line_1": "Phyrexia: All Will Be One",
        "text_line_2": "ONE - June 2023",
        "set_icon": "mtglabels/templates/pips/multi.svg",
        "colour_icon": "mtglabels/templates/pips/g.svg",
    },
    {
        "text_line_1": "Phyrexia: All Will Be One",
        "text_line_2": "ONE - June 2023",
        "set_icon": "mtglabels/templates/pips/multi.svg",
        "colour_icon": "mtglabels/templates/pips/r.svg",
    },
    {
        "text_line_1": "Phyrexia: All Will Be One",
        "text_line_2": "ONE - June 2023",
        "set_icon": "mtglabels/templates/pips/multi.svg",
        "colour_icon": "mtglabels/templates/pips/c.svg",
    },
    {
        "text_line_1": "Phyrexia: All Will Be One",
        "text_line_2": "ONE - June 2023",
        "set_icon": "mtglabels/templates/pips/multi.svg",
        "colour_icon": "mtglabels/templates/pips/w.svg",
    },
]

template_offsets = [
    {
        "x_offset": col * divider_width + page_offset,
        "y_offset": row * divider_height + page_offset,
    }
    for row in range(labels_per_column)
    for col in range(labels_per_row)
]

template_offsets_cycle = cycle(template_offsets)

dividers = [
    {
        **divider_data,
        **next(template_offsets_cycle),
    }
    for divider_data in card_divider_data
]

label_count = 0

for divider_data in dividers:
    template["text_line_1"] = divider_data["text_line_1"]
    template["text_line_2"] = divider_data["text_line_2"]
    template["set_icon"] = divider_data["set_icon"]
    template["colour_icon"] = divider_data["colour_icon"]

    template.render(offsetx=divider_data["x_offset"], offsety=divider_data["y_offset"])

    new_page_check(label_count)
    label_count += 1

pdf.output("example.pdf")
