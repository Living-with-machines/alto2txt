"""
Functions to convert XML (in METS 1.8/ALTO 1.4, METS 1.3/ALTO 1.4, BLN
or UKP format) publications to plaintext articles and generate minimal
metadata.
"""

import logging
import os
import os.path
import re
from lxml import etree

from alto2txt import xml

logger = logging.getLogger(__name__)
""" Module-level logger. """


def issue_to_text(publication, year, issue, issue_dir, txt_out_dir, xslts):
    """
    Converts a single issue of an XML publication to plaintext
    articles and generates minimal metadata.

    :param publication: Publication directory local name e.g. 0000151
    :type publication: str
    :param year: Year directory local name e.g. 1835
    :type year: str
    :param issue: Issue directory local name e.g. 0121
    :type issue: str
    :param issue_dir: Issue directory e.g. .../0000151/1835/0121
    :type issue_dir: str
    :param txt_out_dir: Output directory for plaintext articles
    :type txt_out_dir: str
    :param xslts: XSLTs to convert XML to plaintext
    :type xslts: dict(str: lxml.etree.XSLT)
    """
    # TODO Fix these error messages, they're too vague
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
    assert not os.path.exists(issue_out_dir) or not os.path.isfile(
        issue_out_dir
    ), "{} exists and is not a file".format(issue_out_dir)
    if not os.path.exists(issue_out_dir):
        os.makedirs(issue_out_dir)
    assert os.path.exists(issue_out_dir), "Create {} failed".format(issue_out_dir)
    for xml_file in os.listdir(issue_dir):
        xml_file_path = os.path.join(issue_dir, xml_file)
        if os.path.isdir(xml_file_path):
            logger.warning("Unexpected directory: %s", xml_file)
            continue
        summary["num_files"] += 1
        if os.path.splitext(xml_file)[1].lower() != ".xml":
            summary["non_xml"] += 1
            logger.warning("File with no .xml suffix: %s", xml_file)
            continue
        try:
            document_tree = xml.get_xml(xml_file_path)
        except Exception as e:
            summary["bad_xml"] += 1
            logger.warning("Problematic file %s: %s", xml_file, str(e))
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
                logger.warning("Unknown METS schema %s: %s", xml_file, mets_uri)
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

            xslt(
                document_tree,
                input_path=etree.XSLT.strparam(os.path.abspath(issue_dir)),
                input_sub_path=etree.XSLT.strparam(input_sub_path),
                input_filename=etree.XSLT.strparam(input_filename),
                output_document_stub=etree.XSLT.strparam(issue_out_stub),
                output_path=etree.XSLT.strparam(issue_out_path),
            )
            summary["converted_ok"] += 1
            logger.info("%s gave XSLT output", xml_file_path)
        except Exception as e:
            summary["converted_bad"] += 1
            logger.error("%s failed to give XSLT output: %s", xml_file, str(e))
            continue
    if (summary["converted_ok"] > 0) and (
        summary["converted_ok"]
        == (
            summary["num_files"]
            - summary["skipped_alto"]
            - summary["skipped_mets_unknown"]
            - summary["skipped_root_unknown"]
            - summary["skipped_bl_page"]
        )
    ):
        logger.info("%s %s", issue_dir, str(summary))
    else:
        logger.warning("%s %s", issue_dir, str(summary))


def publication_to_text(publication_dir, txt_out_dir, xslts, downsample=1):
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
    :type publication_dir: str
    :param txt_out_dir: Output directory for plaintext articles
    :type txt_out_dir: str
    :param xslts: XSLTs to convert XML to plaintext
    :type xslts: dict(str: lxml.etree.XSLT)
    :param downsample: Downsample, converting every Nth issue only
    :type downsample: int
    """
    issue_counter = 0

    # TODO The publication name, year, and edition is copied from the directory path and not the METS file.

    publication = os.path.basename(publication_dir)
    logger.info("Processing publication: %s", publication)
    for year in os.listdir(publication_dir):
        year_dir = os.path.join(publication_dir, year)
        if not os.path.isdir(year_dir):
            logger.warning("Unexpected file: %s", year)
            continue
        for issue in os.listdir(year_dir):
            issue_dir = os.path.join(year_dir, issue)
            if not os.path.isdir(issue_dir):
                logger.warning("Unexpected file: %s", os.path.join(year, issue))
                continue
            # Only process every Nth issue (when using downsample).
            issue_counter += 1
            if (issue_counter % downsample) != 0:
                continue
            issue_to_text(publication, year, issue, issue_dir, txt_out_dir, xslts)


def publications_to_text(publications_dir, txt_out_dir, downsample=1):
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
            logger.warning("Unexpected file: %s", publication_dir)
            continue
        publication_txt_out_dir = os.path.join(txt_out_dir, publication)
        publication_to_text(publication_dir, publication_txt_out_dir, xslts, downsample)
