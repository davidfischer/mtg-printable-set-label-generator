Magic: the Gathering Printable Set Divider Generator
==================================================

This is a small script used to generate divirders that can be used to sort
your Magic: the Gathering (MTG) collection.
The code is powered by the [Scryfall API][scryfall-api].
As soon as a new set is up on Scryfall,
the label for that set can be generated and printed.

* Print set dividers
* Cut out the dividers
* Sort your collection

[scryfall-api]: https://scryfall.com/docs/api/sets

## Usage
<!--
If you're just interested in downloading and printing these set labels,
check out the [web frontend](https://mtg-label-generator.fly.dev/)
([code](https://github.com/davidfischer/mtg-printable-set-label-frontend))
and generate your own labels. -->

The script `generator.py` is a small Python script to generate the printable labels.
It requires Python 3.10+ and has a few dependencies.

```shell
python -m venv .venv # Create a new Python virtual environment`
source .venv/bin/activate # Activate the virtual environment
pip install -r requirements.txt # Install the requirements
python mtglabels/generator.py --help # Run the script
```

<!-- ### Customizing

A lot of features can be customized by changing constants at the top of `generator.py`.
For example, sets can be excluded one-by-one or in groups by type or sets can be renamed.

The labels are designed for US Letter paper but this can be customized:

    python mtglabels/generator.py --paper-size=a4   # Use A4 paper size
    python mtglabels/generator.py --help   # Show all options

You can generate labels for specific sets as well:

    python mtglabels/generator.py lea mh1 mh2 neo


You can change how the labels are actually displayed and rendered by customizing `templates/labels.svg`.
If you change the fonts, you may also need to resize things to fit. -->


## License

The code is available at [GitHub][home] under the [MIT license][license].

Some data such as set icons are unofficial Fan Content permitted under the Wizards of the Coast Fan Content Policy
and is copyright Wizards of the Coast, LLC, a subsidiary of Hasbro, Inc.
This code is not produced by, endorsed by, supported by, or affiliated with Wizards of the Coast.

[home]: https://github.com/smithjw/mtg-printable-set-label-generator
[license]: https://opensource.org/licenses/MIT


## Credits

Thank you to the other projects that inspired this project along with the [original repo][original-repo] I forked this from:

- [@davidfischer](https://github.com/davidfischer) - [mtg-printable-set-label-generator][original-repo]
- [@xsilium](https://github.com/xsilium) - [MTG-Printable-Labels](https://github.com/xsilium/MTG-Printable-Labels)

[original-repo]: https://github.com/davidfischer/mtg-printable-set-label-generator
