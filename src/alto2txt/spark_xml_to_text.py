"""
Functions to convert XML (in METS 1.8/ALTO 1.4, METS 1.3/ALTO 1.4, BLN
or UKP format) publications to plaintext articles and generate minimal
metadata using Apache Spark.
"""

import logging
import logging.config
import os
import os.path
from pyspark import SparkContext, SparkConf

from alto2txt.logging_utils import configure_logging
from alto2txt import xml
from alto2txt import xml_to_text

LOG_FILE = "logging.config"
""" Default log file name. """

logger = logging.getLogger(__name__)
""" Module-level logger. """


def publication_to_text(
    publications_dir, publication, txt_out_dir, log_file, downsample=1
):
    """
    Converts issues of an XML publication to plaintext articles and
    generates minimal metadata.

    Loads XSLTs, checks publications_dir/publication exists then calls
    xml_to_text.publication_to_text.

    :param publications_dir: Input directory with XML publications
    :type publications_dir: str
    :param publication: Local publication directory in publications_dir
    :type publication: str
    :param txt_out_dir: Output directory for plaintext articles
    :type txt_out_dir: str
    :param log_file: log file
    :type log_file: str
    :param downsample: Downsample, converting every Nth issue only
    :type downsample: int
    """
    # This function will run on Spark worker node so reconfigure
    # logging.
    configure_logging(log_file)
    xslts = xml.load_xslts()
    publication_dir = os.path.join(publications_dir, publication)
    if not os.path.isdir(publication_dir):
        logger.warning("Unexpected file: %s", publication_dir)
        return
    publication_txt_out_dir = os.path.join(txt_out_dir, publication)
    xml_to_text.publication_to_text(
        publication_dir, publication_txt_out_dir, xslts, downsample
    )


def publications_to_text(
    publications_dir, txt_out_dir, log_file, num_cores=1, downsample=1
):
    """
    Converts XML publications to plaintext articles and generates
    minimal metadata.

    Each publication is processed concurrently via Spark.

    publications_dir is expected to hold XML for multiple
    publications, in the following structure:

    publications_dir
    |-- publication
    |   |-- year
    |   |   |-- issue
    |   |   |   |-- xml_content
    |   |-- year
    |-- publication

    txt_out_dir is created with an analogous structure.

    Quality assurance is also performed to check for:

    * Unexpected directories.
    * Unexpected files.
    * Malformed XML.
    * Empty files.
    * Files that otherwise do not expose content.

    The following XSLT files need to be in an extract_text.xslts
    module:

    * extract_text_mets18.xslt: METS 1.8 XSL file.
    * extract_text_mets13.xslt: METS 1.3 XSL file.
    * extract_text_bln.xslt: BLN XSL file.
    * extract_text_ukp.xslt: UKP XSL file.

    :param publications dir: Input directory with XML publications
    :type publications_dir: str
    :param txt_out_dir: Output directory for plaintext articles
    :type txt_out_dir: str
    :param log_file: log file
    :type log_file: str
    :param num_cores: Number of cores
    :type num_cores: int
    :param downsample: Downsample, converting every Nth issue only
    :type downsample: int
    """
    logger.info("Processing: %s", publications_dir)
    publications = os.listdir(publications_dir)
    conf = SparkConf()
    conf.setAppName(__name__)
    conf.set("spark.cores.max", num_cores)
    context = SparkContext(conf=conf)
    rdd_publications = context.parallelize(publications, num_cores)
    rdd_publications = context.parallelize(publications)
    rdd_publications.map(
        lambda publication: publication_to_text(
            publications_dir, publication, txt_out_dir, log_file, downsample
        )
    ).collect()
