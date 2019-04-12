#!/usr/bin/env python
"""
Convert a single newspaper's XML (in METS 1.8/ALTO 1.4, BLN or UKP
format) to plaintext articles and generate minimal
metadata. Downsampling can be used to convert only every Nth issue of
the newspaper. One text file is output per article.

Quality assurance will also be performed to check:

* Unexpected directories.
* Unexpected files.
* Malformed XML.
* Empty files.
* Files that otherwise do not expose content.

    usage: extract_publication_text.py [-h]
                           [-d [DOWNSAMPLE]] [-x [XSLT_FILE]]
                           publication_dir txt_out_dir

    Extract plaintext articles from newspaper XML

    positional arguments:
      publication_dir       Publication directory with XML
      txt_out_dir           Output directory with plaintext

    optional arguments:
      -h, --help            show this help message and exit
      -d [DOWNSAMPLE], --downsample [DOWNSAMPLE]
                            Downsample
      -x [XSLT_FILE], --xslt_file [XSLT_FILE]
                            XSLT file to convert XML to plaintext

publication_dir is expected to have structure:

    publication_dir
    |-- year
    |   |-- issue
    |   |   |-- xml_content
    |-- year

txt_out_dir is created with an analogous structure.

XSLT_FILE must be an XSLT file, default, "extract_text.xslt".

DOWNSAMPLE must be a positive integer, default 1.
"""

from argparse import ArgumentParser
from extract_text import XSLT_FILENAME
from extract_text import xml_publication_to_text


def main():
    """
    Convert a single newspaper's XML (in METS 1.8/ALTO 1.4, BLN or UKP
    format) to plaintext articles and generate minimal metadata.

    Parse command-line arguments and call
    extract_text.xml_publication_to_text.
    """
    parser = ArgumentParser(
        description="Extract plaintext articles from newspaper XML")
    parser.add_argument("publication_dir",
                        help="Publication directory with XML")
    parser.add_argument("txt_out_dir",
                        help="Output directory with plaintext")
    parser.add_argument("-d",
                        "--downsample",
                        type=int,
                        nargs="?",
                        default=1,
                        help="Downsample")
    parser.add_argument("-x",
                        "--xslt_file",
                        nargs="?",
                        default=XSLT_FILENAME,
                        help="XSLT file to convert XML to plaintext")
    args = parser.parse_args()
    publication_dir = args.publication_dir
    txt_out_dir = args.txt_out_dir
    xslt_file = args.xslt_file
    downsample = args.downsample
    xml_publication_to_text(publication_dir,
                            txt_out_dir,
                            xslt_file,
                            downsample)


if __name__ == "__main__":
    main()
