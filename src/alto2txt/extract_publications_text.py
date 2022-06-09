#!/usr/bin/env python
"""
Converts XML (in METS 1.8/ALTO 1.4, METS 1.3/ALTO 1.4, BLN or UKP
format) publications to plaintext articles and generates minimal
metadata. Downsampling can be used to convert only every Nth issue of
each newspaper. One text file is output per article, each complemented
by one XML metadata file.

Quality assurance is also performed to check for:

* Unexpected directories.
* Unexpected files.
* Malformed XML.
* Empty files.
* Files that otherwise do not expose content.

Usage:

    usage: extract_publications_text.py [-h] [-p [PROCESS_TYPE]]
                                        [-l [LOG_FILE]]
                                        [-d [DOWNSAMPLE]]
                                        [-n [NUM_CORES]]
                                        xml_in_dir txt_out_dir

    Converts XML publications to plaintext articles

    positional arguments:
      xml_in_dir            Input directory with XML publications
      txt_out_dir           Output directory for plaintext articles

    optional arguments:
      -h, --help            show this help message and exit
      -p [PROCESS_TYPE], --process-type [PROCESS_TYPE]
                            Process type. One of: single,serial,multi,spark
                            Default: multi
      -l [LOG_FILE], --log-file [LOG_FILE]
                            Log file. Default out.log
      -d [DOWNSAMPLE], --downsample [DOWNSAMPLE]
                            Downsample. Default 1
      -n [NUM_CORES], --num-cores [NUM_CORES]
                            Number of cores (Spark only). Default 1")

xml_in_dir is expected to hold XML for multiple publications, in the
following structure:

    xml_in_dir
    |-- publication
    |   |-- year
    |   |   |-- issue
    |   |   |   |-- xml_content
    |   |-- year
    |-- publication

However, if "-p|--process-type single" is provided then xml_in_dir is
expected to hold XML for a single publication, in the following
structure:

    xml_in_dir
    |-- year
    |   |-- issue
    |   |   |-- xml_content
    |-- year

txt_out_dir is created with an analogous structure to xml_in_dir.

PROCESS_TYPE can be one of:

* single: Process single publication.
* serial: Process publications serially.
* multi: Process publications using multiprocessing (default).
* spark: Process publications using Spark.

DOWNSAMPLE must be a positive integer, default 1.

The following XSLT files need to be in an extract_text.xslts module:

* extract_text_mets18.xslt: METS 1.8 XSL file.
* extract_text_mets13.xslt: METS 1.3 XSL file.
* extract_text_bln.xslt: BLN XSL file.
* extract_text_ukp.xslt: UKP XSL file.
"""

from argparse import ArgumentParser

from alto2txt import xml_to_text_entry


def main():
    """
    Converts XML publications to plaintext articles and generates
    minimal metadata.

    Parses command-line arguments and calls
    extract_text.xml_publications_to_text.
    """
    parser = ArgumentParser(
        description="Converts XML publications to plaintext articles"
    )
    parser.add_argument("xml_in_dir", help="Input directory with XML publications")
    parser.add_argument("txt_out_dir", help="Output directory for plaintext articles")
    parser.add_argument(
        "-p",
        "--process-type",
        type=str,
        nargs="?",
        default=xml_to_text_entry.PROCESS_MULTI,
        help="Process type. One of: "
        + ",".join(xml_to_text_entry.PROCESS_TYPES)
        + ". Default: multi",
    )
    parser.add_argument(
        "-l",
        "--log-file",
        type=str,
        nargs="?",
        default="out.log",
        help="Log file. Default out.log",
    )
    parser.add_argument(
        "-d",
        "--downsample",
        type=int,
        nargs="?",
        default=1,
        help="Downsample. Default 1",
    )
    parser.add_argument(
        "-n",
        "--num-cores",
        type=int,
        nargs="?",
        default=1,
        help="Number of cores (Spark only). Default 1",
    )
    args = parser.parse_args()
    xml_in_dir = args.xml_in_dir
    txt_out_dir = args.txt_out_dir
    process_type = args.process_type
    log_file = args.log_file
    num_cores = args.num_cores
    downsample = args.downsample
    xml_to_text_entry.xml_publications_to_text(
        xml_in_dir, txt_out_dir, process_type, log_file, num_cores, downsample
    )


if __name__ == "__main__":
    main()
