#!/usr/bin/env python
"""
Convert multiple newspapers' XML (in METS 1.8/ALTO 1.4, METS 1.3/ALTO
1.4, BLN or UKP format) to plaintext articles and generate minimal
metadata. Downsampling can be used to convert only every Nth issue of
each newspaper. One text file is output per article, each complemented
by one XML metadata file.

Quality assurance will also be performed to check:

* Unexpected directories.
* Unexpected files.
* Malformed XML.
* Empty files.
* Files that otherwise do not expose content.

    usage: extract_publications_text.py [-h]
                           [-d [DOWNSAMPLE]]
                           publications_dir txt_out_dir

    Extract plaintext articles from multiple newspapers' XML

    positional arguments:
      publications_dir      Publications directory with XML
      txt_out_dir           Output directory with plaintext

    optional arguments:
      -h, --help            show this help message and exit
      -d [DOWNSAMPLE], --downsample [DOWNSAMPLE]
                            Downsample

publications_dir is expected to have structure:

    publications_dir
    |-- publication
    |   |-- year
    |   |   |-- issue
    |   |   |   |-- xml_content
    |   |-- year

txt_out_dir is created with an analogous structure.

DOWNSAMPLE must be a positive integer, default 1.

The following XSLT files need to be in the current directory:

* extract_text_mets18.xslt: METS 1.8 XSL file.
* extract_text_mets13.xslt: METS 1.3 XSL file.
* extract_text_bln.xslt: BLN XSL file.
* extract_text_ukp.xslt: UKP XSL file.
"""

from argparse import ArgumentParser
from extract_text import xml_publications_to_text


def main():
    """
    Convert multiple newspapers' XML (in METS 1.8/ALTO 1.4, METS
    1.3/ALTO 1.4, BLN or UKP format) to plaintext articles and
    generate minimal metadata.

    Parse command-line arguments and call
    extract_text.xml_publications_to_text.
    """
    parser = ArgumentParser(
        description="Extract plaintext articles from multiple newspapers' XML")
    parser.add_argument("publications_dir",
                        help="Publications directory with XML")
    parser.add_argument("txt_out_dir",
                        help="Output directory with plaintext")
    parser.add_argument("-d",
                        "--downsample",
                        type=int,
                        nargs="?",
                        default=1,
                        help="Downsample")
    args = parser.parse_args()
    publications_dir = args.publications_dir
    txt_out_dir = args.txt_out_dir
    downsample = args.downsample
    xml_publications_to_text(publications_dir,
                             txt_out_dir,
                             downsample)


if __name__ == "__main__":
    main()
