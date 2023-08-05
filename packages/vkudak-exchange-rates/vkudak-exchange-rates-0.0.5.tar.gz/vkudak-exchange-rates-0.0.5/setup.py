from setuptools import setup, find_packages

VERSION = '0.0.5'

with open("README.md", "r") as f:
    long_description = f.read()

DESCRIPTION = ('A small library for getting information on some currency '
               'exchange rates into UAH, on the selected date')

setup(
    name="vkudak-exchange-rates",
    version=VERSION,
    author="Viktor Kudak",
    author_email="vkudak@gmail.com",
    license='MIT',
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",

    install_requires=['requests', 'matplotlib', 'pandas'],

    package_dir={"": "vkudak_exchange_rates"},  # Optional
    # You can just specify package directories manually here if your project is
    # simple. Or you can use find_packages().
    #
    # Alternatively, if you just want to distribute a single Python file, use
    # the `py_modules` argument instead as follows, which will expect a file
    # called `my_module.py` to exist:
    #
    #   py_modules=["my_module"],
    #
    packages=find_packages(where="vkudak_exchange_rates", exclude=("tests",)),  # Required

    keywords=['python', 'exchange rate'],
    classifiers=[
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    project_urls={
        'Source': 'https://gtlb.jetsoftpro.com/vkudak/vkudak-exchange-rates',
    },
)
