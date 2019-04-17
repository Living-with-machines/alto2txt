"""
Functions to convert XML (in METS 1.8/ALTO 1.4, METS 1.3/ALTO 1.4, BLN
or UKP format) publications to plaintext articles and generate minimal
metadata.
"""

from __future__ import print_function
import logging
import logging.config
import os
import os.path

from extract_text.logging_utils import configure_logging
from extract_text import xml
from extract_text import xml_to_text

logger = logging.getLogger(__name__)
""" Module-level logger. """

PROCESS_SINGLE = "single"
""" Process single publication. """
PROCESS_SERIAL = "serial"
""" Process publications serially. """
PROCESS_MULTI = "multi"
""" Process publications using multiprocessing. """
PROCESS_SPARK = "spark"
""" Process publications using Spark. """
PROCESS_TYPES = [PROCESS_SINGLE,
                 PROCESS_SERIAL,
                 PROCESS_MULTI,
                 PROCESS_SPARK]


def check_parameters(xml_in_dir, txt_out_dir, process_type, downsample):
    """
    Check parameters. The following checks are done:

    * xml_in_dir exists and is a directory.
    * txt_out_dir either does not exists or exists and is a directory.
    * xml_in_dir and txt_out_dir are not the same directory.
    * process_type is one of single, serial, multi, spark.
    * downsample is a positive integer.

    :param xml_in_dir: Input directory with XML publications
    :type xml_in_dir: str or unicode
    :param txt_out_dir: Output directory for plaintext articles
    :type txt_out_dir: str or unicode
    :param process_type: Process type
    :type process_type: str or unicode
    :param downsample: Downsample
    :type downsample: int
    :raise AssertionError: if any check fails
    """
    assert downsample > 0, "downsample must be a positive integer"
    assert os.path.exists(xml_in_dir),\
        "xml_in_dir, {}, not found".format(xml_in_dir)
    assert os.path.isdir(xml_in_dir),\
        "xml_in_dir, {}, is not a directory".format(xml_in_dir)
    assert not os.path.isfile(txt_out_dir),\
        "txt_out_dir, {}, is not a directory".format(txt_out_dir)
    assert os.path.normpath(xml_in_dir) !=\
        os.path.normpath(txt_out_dir),\
        "xml_in_dir, {}, and txt_out_dir, {}, should be different".\
        format(xml_in_dir, txt_out_dir)
    assert process_type in PROCESS_TYPES,\
        "process-type, {}, must be one of {}.".format(
            process_type,
            ",".join(PROCESS_TYPES))


def xml_publications_to_text(xml_in_dir,
                             txt_out_dir,
                             process_type,
                             log_file="out.log",
                             downsample=1):
    """
    Converts XML publications to plaintext articles and generates
    minimal metadata.

    Each publication is processed concurrently.

    One text file is output per article, each complemented by one XML
    metadata file.

    If is_singleton is True, xml_in_dir is assumed to hold XML for a
    single publication and publication_to_text is called. Otherwise,
    xml_in_dir is assumed to hold XML for multiple publications and
    publications_to_text is called.

    txt_out_dir is created with an analogous structure to xml_in_dir.

    :param xml_in_dir: Input directory with XML publications
    :type xml_in_dir: str or unicode
    :param txt_out_dir: Output directory for plaintext articles
    :type txt_out_dir: str or unicode
    :param process_type: Process type
    :type process_type: str or unicode
    :param log_file: log file
    :type log_file: str or unicode
    :param downsample: Downsample, converting every Nth issue only
    :type downsample: int
    :raise AssertionError: if any parameter check fails (see
    check_parameters)
    """
    check_parameters(xml_in_dir, txt_out_dir, process_type, downsample)
    configure_logging(log_file)
    if process_type == PROCESS_SINGLE:
        xslts = xml.load_xslts()
        xml_to_text.publication_to_text(xml_in_dir,
                                        txt_out_dir,
                                        xslts,
                                        downsample)
    elif process_type == PROCESS_SERIAL:
        xml_to_text.publications_to_text(xml_in_dir,
                                         txt_out_dir,
                                         downsample)
    elif process_type == PROCESS_SPARK:
        from extract_text import spark_xml_to_text
        spark_xml_to_text.publications_to_text(xml_in_dir,
                                               txt_out_dir,
                                               log_file,
                                               downsample)
    else:
        from extract_text import multiprocess_xml_to_text
        multiprocess_xml_to_text.publications_to_text(xml_in_dir,
                                                      txt_out_dir,
                                                      log_file,
                                                      downsample)
