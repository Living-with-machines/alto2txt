"""
Python package configuration file.
"""

import os
from setuptools import setup
from setuptools import find_packages


def read(fname):
    """
    Read and return file contents.

    :param fname: file name
    :type fname: str or unicod
    :returns: file contents
    :rtype: str or unicode
    """
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="extract_text",
    version="0.3.0",
    author="Mike Jackson, David Beavan",
    author_email="mjackson@turing.ac.uk, dbeavan@turing.ac.uk",
    description=("Converts XML publications to plaintext articles."),
    license="Apache License 2.0",
    keywords="XML text processing publications articles",
    url="https://github.com/alan-turing-institute/Living-with-Machines-code",
    packages=find_packages(),
    scripts=["extract_publications_text.py"],
    package_data={'': ['*.xslt']},
    long_description=read("README.md"),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Text Processing",
        "License :: OSI Approved :: Apache Software License",
    ],
)
