Magic: the Gathering Printable Set Label Generator
==================================================

This is a small script for generating Magic: the Gathering (MTG) printable set labels
in order to organize a collection of cards.
The code is powered by the [Scryfall API][scryfall-api].
As soon as a new set is up on Scryfall,
the label for that set can be generated and printed.

* Print and cut out the labels
* Attach set labels to [plastic dividers][plastic-dividers]

<img src="readme-img/organized-cards.jpg">

[scryfall-api]: https://scryfall.com/docs/api/sets
[plastic-dividers]: https://www.amazon.com/dp/B00S3FF1PI/


## Usage

If you're just interested in downloading and printing these set labels,
check out the [releases tab on GitHub][releases] to download and print the PDFs.

If you want to create or customize your own labels, read on!

The script `label-generator.py` is a small Python script to generate the printable labels.
It requires Python 3.6+ and has a few dependencies.


    pip install -r requirements.txt  # Install dependencies
    python label-generator.py        # Creates files in output/

By default, this will create one or more SVG files.
These files are vector image files that can be customized further
or printed using most modern browsers and many other tools.

The SVGs use the free fonts [EB Garamond][garamond] bold and [Source Sans Pro][source-sans] regular.

[releases]: https://github.com/davidfischer/mtg-printable-set-label-generator/releases
[garamond]: https://fonts.google.com/specimen/EB+Garamond
[source-sans]: https://fonts.google.com/specimen/Source+Sans+Pro


### Tips for printing

The output SVGs are precisely sized for a sheet of paper (US Letter by default).
Make sure while printing in your browser or otherwise to set the margins to None.

<img src="readme-img/browser-printing.png">

You can also "print" to a PDF.


### Customizing

A lot of features can be customized by changing constants at the top of `label-generator.py`.
For example, sets can be excluded one-by-one or in groups by type or sets can be renamed.

The labels are designed for US Letter paper but this can be customized.

You can change how the labels are actually displayed and rendered by customizing `templates/labels.svg`.
If you change the fonts, you may also need to resize things to fit.


## License

The code is available at [GitHub][home] under the [MIT license][license].

Some data such as set icons are unofficial Fan Content permitted under the Wizards of the Coast Fan Content Policy
and is copyright Wizards of the Coast, LLC, a subsidiary of Hasbro, Inc.
This code is not produced by, endorsed by, supported by, or affiliated with Wizards of the Coast.

[home]: https://github.com/davidfischer/mtg-printable-set-label-generator
[license]: https://opensource.org/licenses/MIT


## Credits

Special thanks goes to the users behind other printable set labels
such as those found [here][previous-set-labels].
Using these fantastic labels definitely provided inspiration and direction
and made me want something more customizable and updatable.

[previous-set-labels]: https://github.com/xsilium/MTG-Printable-Labels
