"""
Functions to convert XML (in METS 1.8/ALTO 1.4, METS 1.3/ALTO 1.4, BLN
or UKP format) publications to plaintext articles and generate minimal
metadata using multiprocessing.
"""

import logging
import multiprocessing
import os
import os.path
from multiprocessing import Pool

from alto2txt import xml, xml_to_text
from alto2txt.logging_utils import configure_logging

logger = logging.getLogger(__name__)
""" Module-level logger. """


def publication_to_text(
    publications_dir: str,
    publication: str,
    txt_out_dir: str,
    log_file: str,
    downsample: int = 1,
) -> None:
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
    # This function will run in a separate process so reconfigure logging.
    configure_logging(log_file)

    # Load a set of XSLT files
    xslts = xml.load_xslts()

    # Set up the publication_dir
    publication_dir = os.path.join(publications_dir, publication)

    # Check if publication_dir is not a directory
    if not os.path.isdir(publication_dir):
        logger.warning("Unexpected file: %s", publication_dir)
        # TODO: Should this "return" here as well?
        # (see spark_xml_to_text.publication_to_text)

    # Construct a path to the output directory
    publication_txt_out_dir = os.path.join(txt_out_dir, publication)

    # Convert the XML files in the publication directory to plaintext articles
    # using the XSLT files and saves the resulting plaintext articles in the
    # output directory
    xml_to_text.publication_to_text(
        publication_dir, publication_txt_out_dir, xslts, downsample
    )


def publications_to_text(
    publications_dir: str, txt_out_dir: str, log_file: str, downsample: int = 1
) -> None:
    """
    Converts XML publications to plaintext articles and generates
    minimal metadata.

    Each publication is processed concurrently.

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
    :param downsample: Downsample, converting every Nth issue only
    :type downsample: int
    """
    logger.info("Processing: %s", publications_dir)

    # Get publications from list of files in publications_dir
    publications = os.listdir(publications_dir)

    # Set pool size
    pool_size = min(multiprocessing.cpu_count(), len(publications))

    # Log info
    logger.info(
        "Publications: %d CPUs: %d Process pool size: %d",
        len(publications),
        multiprocessing.cpu_count(),
        pool_size,
    )

    # Set up pool for multiprocessing
    pool = Pool(pool_size)

    # Add publication_to_text to pool asynchronously
    for publication in os.listdir(publications_dir):
        pool.apply_async(
            publication_to_text,
            args=(
                publications_dir,
                publication,
                txt_out_dir,
                log_file,
                downsample,
            ),
        )

    # Run the multiprocessing and close
    pool.close()
    pool.join()
