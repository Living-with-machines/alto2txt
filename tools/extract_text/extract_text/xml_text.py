"""
Functions to convert XML (in METS 1.8/ALTO 1.4, METS 1.3/ALTO 1.4, BLN
or UKP format) publications to plaintext articles and generate minimal
metadata. Downsampling can be used to convert only every Nth issue of
each newspaper. One text file is output per article, each complemented
by one XML metadata file.

Quality assurance is also performed to check for:

* Unexpected directories.
* Unexpected files.
* Malformed XML.
* Empty files.
* Files that otherwise do not expose content.

The following XSLT files need to be in an extract_text.xslts module:

* extract_text_mets18.xslt: METS 1.8 XSL file.
* extract_text_mets13.xslt: METS 1.3 XSL file.
* extract_text_bln.xslt: BLN XSL file.
* extract_text_ukp.xslt: UKP XSL file.
"""

from __future__ import print_function
import logging
import logging.config
import multiprocessing
from multiprocessing import Pool
import os
import os.path
import re
from lxml import etree
import yaml

from extract_text import xml

LOG_FILE = "logging.config"
""" Default log file name. """

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


def issue_to_text(publication,
                  year,
                  issue,
                  issue_dir,
                  txt_out_dir,
                  xslts):
    """
    Converts a single issue of an XML publication to plaintext
    articles and generates minimal metadata.

    :param publication: Publication directory local name e.g. 0000151
    :type publication: str or unicode
    :param year: Year directory local name e.g. 1835
    :type year: str or unicode
    :param issue: Issue directory local name e.g. 0121
    :type issue: str or unicode
    :param issue_dir: Issue directory e.g. .../0000151/1835/0121
    :type issue_dir: str or unicode
    :param txt_out_dir: Output directory for plaintext articles
    :type txt_out_dir: str or unicode
    :param xslts: XSLTs to convert XML to plaintext
    :type xslts: dict(str: lxml.etree.XSLT)
    """
    logger.info("Processing issue: %s", os.path.join(year, issue))
    summary = {}
    summary["num_files"] = 0
    summary["bad_xml"] = 0
    summary["converted_ok"] = 0
    summary["converted_bad"] = 0
    summary["skipped_alto"] = 0
    summary["skipped_bl_page"] = 0
    summary["skipped_mets_unknown"] = 0
    summary["skipped_root_unknown"] = 0
    summary["non_xml"] = 0
    issue_out_dir = os.path.join(txt_out_dir, year, issue)
    assert not os.path.exists(issue_out_dir) or\
        not os.path.isfile(issue_out_dir),\
        "{} exists and is not a file".format(issue_out_dir)
    if not os.path.exists(issue_out_dir):
        os.makedirs(issue_out_dir)
    assert os.path.exists(issue_out_dir),\
        "Create {} failed".format(issue_out_dir)
    for xml_file in os.listdir(issue_dir):
        xml_file_path = os.path.join(issue_dir, xml_file)
        if os.path.isdir(xml_file_path):
            logger.warn("Unexpected directory: %s", xml_file)
            continue
        summary["num_files"] += 1
        if os.path.splitext(xml_file)[1].lower() != ".xml":
            summary["non_xml"] += 1
            logger.warn("File with no .xml suffix: %s", xml_file)
            continue
        try:
            document_tree = xml.get_xml(xml_file_path)
        except Exception as e:
            summary["bad_xml"] += 1
            logger.warn("Problematic file %s: %s", xml_file, str(e))
            continue
        metadata = xml.get_xml_metadata(document_tree)
        if metadata[xml.XML_ROOT] == xml.ALTO_ROOT:
            # alto files are accessed via mets file.
            summary["skipped_alto"] += 1
            continue
        if xml.query_xml(document_tree, xml.BLN_PAGE_XPATH):
            # BL_page files contain layout not text.
            summary["skipped_bl_page"] += 1
            continue
        if metadata[xml.XML_ROOT] == xml.BLN_ROOT:
            xslt = xslts[xml.BLN_XSLT]
        elif metadata[xml.XML_ROOT] == xml.UKP_ROOT:
            xslt = xslts[xml.UKP_XSLT]
        elif metadata[xml.XML_ROOT] == xml.METS_ROOT:
            mets_uri = metadata[xml.XML_SCHEMA_LOCATIONS][xml.METS_NS]
            if mets_uri == xml.METS_18_URI:
                xslt = xslts[xml.METS_18_XSLT]
            elif mets_uri == xml.METS_13_URI:
                xslt = xslts[xml.METS_13_XSLT]
            else:
                # Unknown METS.
                logger.warn("Unknown METS schema %s: %s",
                            xml_file,
                            mets_uri)
                summary["skipped_mets_unknown"] += 1
                continue
        else:
            summary["skipped_root_unknown"] += 1
            continue
        input_filename = os.path.basename(xml_file)
        input_sub_path = os.path.join(publication, year, issue)
        if metadata[xml.XML_ROOT] == xml.METS_ROOT:
            mets_match = re.findall(xml.RE_METS, input_filename)
            issue_out_stub = mets_match[0][0]
        else:
            issue_out_stub = os.path.splitext(input_filename)[0]
        issue_out_path = os.path.join(issue_out_dir, issue_out_stub)
        try:
            xslt(document_tree,
                 input_path=etree.XSLT.strparam(issue_dir),
                 input_sub_path=etree.XSLT.strparam(input_sub_path),
                 input_filename=etree.XSLT.strparam(input_filename),
                 output_document_stub=etree.XSLT.strparam(
                     issue_out_stub),
                 output_path=etree.XSLT.strparam(issue_out_path))
            summary["converted_ok"] += 1
            logger.info("%s gave XSLT output", xml_file_path)
        except Exception as e:
            summary["converted_bad"] += 1
            logger.error("%s failed to give XSLT output: %s",
                         xml_file,
                         str(e))
            continue
    if (summary["converted_ok"] > 0) and\
       (summary["converted_ok"] == (summary["num_files"] -
                                    summary["skipped_alto"] -
                                    summary["skipped_mets_unknown"] -
                                    summary["skipped_root_unknown"] -
                                    summary["skipped_bl_page"])):
        logger.info("%s %s", issue_dir, str(summary))
    else:
        logger.warn("%s %s", issue_dir, str(summary))


def publication_to_text(publication_dir,
                        txt_out_dir,
                        xslts,
                        downsample=1):
    """
    Converts issues of an XML publication to plaintext articles and
    generates minimal metadata.

    publication_dir is expected to hold XML for a single publication, in
    the following structure:

    publication_dir
    |-- year
    |   |-- issue
    |   |   |-- xml_content
    |-- year

    txt_out_dir is created with an analogous structure.

    :param publication_dir: Input directory with XML publications
    :type publication_dir: str or unicode
    :param txt_out_dir: Output directory for plaintext articles
    :type txt_out_dir: str or unicode
    :param xslts: XSLTs to convert XML to plaintext
    :type xslts: dict(str: lxml.etree.XSLT)
    :param downsample: Downsample, converting every Nth issue only
    :type downsample: int
    """
    xslts = xml.load_xslts()
    issue_counter = 0
    publication = os.path.basename(publication_dir)
    logger.info("Processing publication: %s", publication)
    for year in os.listdir(publication_dir):
        year_dir = os.path.join(publication_dir, year)
        if not os.path.isdir(year_dir):
            logger.warn("Unexpected file: %s", year)
            continue
        for issue in os.listdir(year_dir):
            issue_dir = os.path.join(year_dir, issue)
            if not os.path.isdir(issue_dir):
                logger.warn("Unexpected file: %s",
                            os.path.join(year, issue))
                continue
            # Only process every Nth issue (when using downsample).
            issue_counter += 1
            if (issue_counter % downsample) != 0:
                continue
            issue_to_text(publication,
                          year,
                          issue,
                          issue_dir,
                          txt_out_dir,
                          xslts)


def publications_to_text(publications_dir,
                         txt_out_dir,
                         downsample=1):
    """
    Converts XML publications to plaintext articles and generates
    minimal metadata.

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

    :param publications dir: Input directory with XML publications
    :type publications_dir: str or unicode
    :param txt_out_dir: Output directory for plaintext articles
    :type txt_out_dir: str or unicode
    :param downsample: Downsample, converting every Nth issue only
    :type downsample: int
    """
    logger.info("Processing: %s", publications_dir)
    xslts = xml.load_xslts()
    publications = os.listdir(publications_dir)
    logger.info("Publications: %d", len(publications))
    for publication in publications:
        publication_dir = os.path.join(publications_dir, publication)
        if not os.path.isdir(publication_dir):
            logger.warn("Unexpected file: %s", publication_dir)
            continue
        publication_txt_out_dir = os.path.join(txt_out_dir, publication)
        publication_to_text(publication_dir,
                            publication_txt_out_dir,
                            xslts,
                            downsample)


def publication_to_text_multiprocessing(publications_dir,
                                        publication,
                                        txt_out_dir,
                                        downsample=1):
    """
    Converts issues of an XML publication to plaintext articles and
    generates minimal metadata.

    Loads XSLTs, checks publications_dir/publication exists then calls
    publication_to_text.

    :param publications_dir: Input directory with XML publications
    :type publications_dir: str or unicode
    :param publication: Local publication directory in publications_dir
    :type publication: str or unicode
    :param txt_out_dir: Output directory for plaintext articles
    :type txt_out_dir: str or unicode
    :param downsample: Downsample, converting every Nth issue only
    :type downsample: int
    """
    xslts = xml.load_xslts()
    publication_dir = os.path.join(publications_dir, publication)
    if not os.path.isdir(publication_dir):
        logger.warn("Unexpected file: %s", publication_dir)
    publication_txt_out_dir = os.path.join(txt_out_dir, publication)
    publication_to_text(publication_dir,
                        publication_txt_out_dir,
                        xslts,
                        downsample)


def publications_to_text_multiprocessing(publications_dir,
                                         txt_out_dir,
                                         downsample=1):
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

    :param publications dir: Input directory with XML publications
    :type publications_dir: str or unicode
    :param txt_out_dir: Output directory for plaintext articles
    :type txt_out_dir: str or unicode
    :param downsample: Downsample, converting every Nth issue only
    :type downsample: int
    """
    logger.info("Processing: %s", publications_dir)
    publications = os.listdir(publications_dir)
    pool_size = min(multiprocessing.cpu_count(), len(publications))
    logger.info("Publications: %d CPUs: %d Process pool size: %d",
                len(publications),
                multiprocessing.cpu_count(),
                pool_size)
    pool = Pool(pool_size)
    for publication in os.listdir(publications_dir):
        pool.apply_async(publication_to_text_multiprocessing,
                         args=(publications_dir,
                               publication,
                               txt_out_dir,
                               downsample))
    pool.close()
    pool.join()


def publication_to_text_spark(publications_dir,
                              publication,
                              txt_out_dir,
                              downsample=1):
    """
    Converts issues of an XML publication to plaintext articles and
    generates minimal metadata.

    Checks pulications_dir/publication exists then calls
    publication_to_text.

    :param publications_dir: Input directory with XML publications
    :type publications_dir: str or unicode
    :param publication: Local publication directory in publications_dir
    :type publication: str or unicode
    :param txt_out_dir: Output directory for plaintext articles
    :type txt_out_dir: str or unicode
    :param downsample: Downsample, converting every Nth issue only
    :type downsample: int
    """
    publication_dir = os.path.join(publications_dir, publication)
    if not os.path.isdir(publication_dir):
        logger.warn("Unexpected file: %s", publication_dir)
        return "XXX"
    publication_txt_out_dir = os.path.join(txt_out_dir, publication)
    publication_to_text(publication_dir,
                        publication_txt_out_dir,
                        downsample)
    return publication


def publications_to_text_spark(publications_dir,
                               txt_out_dir,
                               downsample=1):
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

    :param publications dir: Input directory with XML publications
    :type publications_dir: str or unicode
    :param txt_out_dir: Output directory for plaintext articles
    :type txt_out_dir: str or unicode
    :param downsample: Downsample, converting every Nth issue only
    :type downsample: int
    """
    from pyspark import SparkContext, SparkConf

    logger.info("Processing: %s", publications_dir)
    publications = os.listdir(publications_dir)
    # TODO make num_cores configurable
    num_cores = 144
    conf = SparkConf()
    conf.setAppName("xml_text")
    conf.set("spark.cores.max", num_cores)
    context = SparkContext(conf=conf)
    log = context._jvm.org.apache.log4j.LogManager.getLogger(__name__)  # pylint: disable=protected-access
    rdd_publications = context.parallelize(publications, num_cores)
    done = rdd_publications.map(
        lambda publication: publication_to_text_spark(
            publications_dir,
            publication,
            txt_out_dir,
            downsample)).collect()
    logger.info("DONE: %s", str(done))


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
    :param downsample: Downsample, converting every Nth issue only
    :type downsample: int
    :param is_singleton: xml_in_dir holds XML for a single publication
    (True) or multiple publications (False)
    :type is_singleton: bool
    :raise AssertionError: if any parameter check fails (see
    check_parameters)
    """
    check_parameters(xml_in_dir, txt_out_dir, process_type, downsample)
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            logging.config.dictConfig(yaml.load(f))
    else:
        logging.basicConfig(level=logging.INFO)
    if process_type == PROCESS_SINGLE:
        publication_to_text(xml_in_dir,
                            txt_out_dir,
                            downsample)
    elif process_type == PROCESS_SERIAL:
        publications_to_text(xml_in_dir,
                             txt_out_dir,
                             downsample)
    elif process_type == PROCESS_SPARK:
        publications_to_text_spark(xml_in_dir,
                                   txt_out_dir,
                                   downsample)
    else:
        publications_to_text_multiprocessing(xml_in_dir,
                                             txt_out_dir,
                                             downsample)