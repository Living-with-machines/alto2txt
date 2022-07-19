"""
Python package configuration file.
"""

import os

from setuptools import find_packages, setup


def read(fname):
    """
    Read and return file contents.

    :param fname: file name
    :type fname: str
    :returns: file contents
    :rtype: str
    """
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="alto2txt",
    version="0.3.0",
    author="Mike Jackson, David Beavan",
    author_email="mjackson@turing.ac.uk, dbeavan@turing.ac.uk",
    description=("Converts XML publications to plaintext articles."),
    license="MIT",
    keywords="XML text processing publications articles",
    url="https://github.com/alan-turing-institute/Living-with-Machines-code",
    packages=find_packages(),
    scripts=["src/alto2txt/extract_publications_text.py"],
    package_data={"": ["*.xslt"]},
    long_description=read("README.md"),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Text Processing",
        "License :: OSI Approved :: MIT License",
    ],
)
