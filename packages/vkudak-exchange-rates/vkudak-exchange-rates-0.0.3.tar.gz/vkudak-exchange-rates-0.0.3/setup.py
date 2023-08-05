from setuptools import setup, find_packages

VERSION = '0.0.3'

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

    packages=find_packages(exclude=("tests",)),
    install_requires=['requests', 'matplotlib', 'pandas'],

    keywords=['python', 'exchange rate'],
    classifiers=[
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    project_urls={
        'Source': 'https://github.com/vkudak/vkudak-exchange-rates',
    },
)
