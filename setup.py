from setuptools import setup


setup(
    name='mtg-printable-set-label-generator',
    version='0.0.1',
    install_requires=[
        "Jinja2>=3,<4",
        "requests>=2.22.0,<3",
        "CairoSVG>=2.5,<3",
    ],
    py_modules=['mtglabels'],
    package_data={'': ['*.svg']},
    include_package_data=True,
    entry_points={
        'console_scripts': ['mtglabels=mtglabels:main'],
    },
)