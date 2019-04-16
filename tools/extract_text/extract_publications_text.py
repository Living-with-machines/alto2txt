#!/usr/bin/env python
"""
Converts XML (in METS 1.8/ALTO 1.4, METS 1.3/ALTO 1.4, BLN or UKP
format) publications to plaintext articles and generates minimal
metadata. Downsampling can be used to convert only every Nth issue of
each newspaper. One text file is output per article, each complemented
by one XML metadata file.

Each publication is processed concurrently.

Quality assurance is also performed to check for:

* Unexpected directories.
* Unexpected files.
* Malformed XML.
* Empty files.
* Files that otherwise do not expose content.

Usage:

    extract_publications_text.py [-h] [-d [DOWNSAMPLE]] [-s]
                                  xml_in_dir txt_out_dir

    positional arguments:
      xml_in_dir            Input directory with XML publications
      txt_out_dir           Output directory for plaintext articles

    optional arguments:
      -h, --help            show this help message and exit
      -d [DOWNSAMPLE], --downsample [DOWNSAMPLE]
                            Downsample
      -s, --singleton       Specify that xml_in_dir holds XML for a single
                            publication

xml_in_dir is expected to hold XML for multiple publications, in the
following structure:

    xml_in_dir
    |-- publication
    |   |-- year
    |   |   |-- issue
    |   |   |   |-- xml_content
    |   |-- year
    |-- publication

However, if "-s"|"--single" is provided then xml_in_dir is expected to
hold XML for a single publication, in the following structure:

    xml_in_dir
    |-- year
    |   |-- issue
    |   |   |-- xml_content
    |-- year

txt_out_dir is created with an analogous structure to xml_in_dir.

DOWNSAMPLE must be a positive integer, default 1.

The following XSLT files need to be in an extract_text.xslts module:

* extract_text_mets18.xslt: METS 1.8 XSL file.
* extract_text_mets13.xslt: METS 1.3 XSL file.
* extract_text_bln.xslt: BLN XSL file.
* extract_text_ukp.xslt: UKP XSL file.
"""

from argparse import ArgumentParser
from extract_text.xml_text import xml_publications_to_text


def main():
    """
    Converts XML publications to plaintext articles and generates
    minimal metadata.

    Parses command-line arguments and calls
    extract_text.xml_publications_to_text.
    """
    parser = ArgumentParser(
        description="Converts XML publications to plaintext articles")
    parser.add_argument("xml_in_dir",
                        help="Input directory with XML publications")
    parser.add_argument("txt_out_dir",
                        help="Output directory for plaintext articles")
    parser.add_argument("-d",
                        "--downsample",
                        type=int,
                        nargs="?",
                        default=1,
                        help="Downsample")
    parser.add_argument(
        "-s",
        "--singleton",
        action='store_true',
        help="Specify that xml_in_dir holds XML for a single publication")
    args = parser.parse_args()
    xml_in_dir = args.xml_in_dir
    txt_out_dir = args.txt_out_dir
    downsample = args.downsample
    is_singleton = args.singleton
    xml_publications_to_text(xml_in_dir,
                             txt_out_dir,
                             is_singleton,
                             downsample)


if __name__ == "__main__":
    main()
