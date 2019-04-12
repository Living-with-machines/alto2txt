#!/usr/bin/env python
"""
Functions to convert a single newspaper's XML (in METS 1.8/ALTO 1.4,
BLN or UKP format) to plaintext articles and generate minimal
metadata.
"""

from __future__ import print_function
import os
import os.path
import re
import sys
from lxml import etree

XSLT_FILENAME = "extract_text.xslt"
""" Default XSL filename """

XSI_NS = "http://www.w3.org/2001/XMLSchema-instance"
""" XML Schema Instance namespace """
SCHEMA_LOCATION = etree.QName(XSI_NS, "schemaLocation")
""" schemaLocation element """
NO_NS_SCHEMA_LOCATION = etree.QName(XSI_NS,
                                    "noNamespaceSchemaLocation")
""" noNamespaceSchemaLocation element """

UKP_NS = "http://tempuri.org/ncbpissue"
""" UKP namespace """
UKP_ROOT = etree.QName(UKP_NS, "UKP")
""" UKP root element """
METS_NS = "http://www.loc.gov/METS/"
""" METS namespace """
METS_ROOT = etree.QName(METS_NS, "mets")
""" METS root element """
ALTO_ROOT = "alto"
""" ALTO root element """
BLN_PAGE_XPATH = "/BL_newspaper/BL_page"
""" XPath for BLN BL_page element """

LWM_NS = {
    'ukp': UKP_NS,
    'mets': METS_NS
}
""" Namespaces of documents within Living with Machines datasets. """

XML_ROOT = "root"
""" XML metadata key. """
XML_DOCTYPE = "doctype"
""" XML metadata key. """
XML_NS = "namespaces"
""" XML metadata key. """
XML_NO_NS_SCHEMA_LOCATION = "no_ns_schema_location"
""" XML metadata key. """
XML_SCHEMA_LOCATIONS = "schema_locations"
""" XML metadata key. """

RE_METS = "(.*)[-|_](mets|METS).xml$"
""" Regular expression for METS file """


def get_xml(filename):
    """
    Get XML document tree from file.

    :param filename: XML filename
    :type filename: str or unicode
    :return: Document tree
    :rtype: lxml.etree._ElementTree
    """
    with open(filename, "r") as f:
        document_tree = None
        parser = etree.XMLParser()
        document_tree = etree.parse(f, parser)
    return document_tree


def get_xml_metadata(document_tree):
    """
    Extract information (root element, namespaces, schema locations,
    default schema location) from XML file. Returns dict of form:

        {
            doctype: <DOCTYPE>,
            namespaces: {TAG: URL, TAG: URL, ...},
            no_ns_schema_location: <URL> | None,
            root: <ROOT_ELEMENT>,
            schema_locations: [URL, URL, ...] | None
        }

    :param document_tree: Document tree
    :type document_tree: lxml.etree._ElementTree
    :return: metadata
    :rtype: dict
    """
    root_element = document_tree.getroot()
    root_element_tag = str(root_element.tag)
    doctype = str(document_tree.docinfo.doctype)
    namespaces = root_element.nsmap
    no_ns_schema_location = root_element.get(NO_NS_SCHEMA_LOCATION.text)
    schema_locations = root_element.get(SCHEMA_LOCATION.text)
    if schema_locations is not None:
        schema_locations = schema_locations.split(" ")

    metadata = {}
    metadata[XML_ROOT] = root_element_tag
    metadata[XML_DOCTYPE] = doctype
    metadata[XML_NS] = namespaces
    metadata[XML_NO_NS_SCHEMA_LOCATION] = no_ns_schema_location
    metadata[XML_SCHEMA_LOCATIONS] = schema_locations
    return metadata


def query_xml(document_tree, query):
    """
    Run XPath query and return results.

    Query string can use namespace prefixes of "ukp" and "mets"
    (as defined in LWM_NS).

    :param document_tree: Document tree
    :type document_tree: lxml.etree._ElementTree
    :param query: XPath query
    :type query: str or unicode
    :return: Query results
    :rtype: Query-specific
    """
    root_element = document_tree.getroot()
    result = root_element.xpath(query, namespaces=LWM_NS)
    return result


def xml_publication_to_text(publication_dir,
                            txt_out_dir,
                            xslt_file=XSLT_FILENAME,
                            downsample=1):
    """
    Convert a single newspaper's XML (in METS 1.8/ALTO 1.4, BLN or UKP
    format) to plaintext articles and generate minimal metadata.
    Downsampling can be used to convert only every Nth issue of the
    newspaper. One text file is output per article.

    Quality assurance will also be performed to check:

    * Unexpected directories.
    * Unexpected files.
    * Malformed XML.
    * Empty files.
    * Files that otherwise do not expose content.

    publication_dir is expected to have structure:

        publication_dir
        |-- year
        |   |-- issue
        |   |   |-- xml_content
        |-- year

    txt_out_dir is created with an analogous structure.

    xslt_file must be an XSLT file, default, "extract_text.xslt".

    downsample must be a positive integer, default 1.

    :param publication_dir: Publication directory with XML
    :type publication_dir: str or unicode
    :param txt_out_dir: Output directory with plaintext
    :type txt_out_dir: str or unicode
    :param xslt_file: XSLT file to convert XML to plaintext
    :type xslt_file: str or unicode
    :param downsample: Downsample
    :type downsample: int
    :raise AssertionError: if any parameter check fails (see
    check_parameters)
    """
    check_parameters(publication_dir,
                     txt_out_dir,
                     xslt_file,
                     downsample)
    xslt_dom = etree.parse(xslt_file)
    xslt = etree.XSLT(xslt_dom)
    issue_counter = 0
    publication = os.path.basename(publication_dir)
    print("INFO: processing publication: {}".format(publication))
    for year in os.listdir(publication_dir):
        year_dir = os.path.join(publication_dir, year)
        if not os.path.isdir(year_dir):
            print("WARN: unexpected file: {}".format(year))
            continue
        for issue in os.listdir(year_dir):
            issue_dir = os.path.join(year_dir, issue)
            if not os.path.isdir(issue_dir):
                print("WARN: unexpected file: {}".format(issue))
                continue
            # Only process every nth (when using downsample).
            issue_counter += 1
            if (issue_counter % downsample) != 0:
                continue
            print("INFO: processing issue in dir: {}".format(issue_dir))
            # Reset per issue stats
            num_files = 0
            bad_xml = 0
            converted_ok = 0
            converted_bad = 0
            non_xml = 0
            skipped_alto = 0
            skipped_bl_page = 0
            # Make output directories for plain text and metadata.
            output_path = os.path.join(txt_out_dir, year, issue)
            assert not os.path.exists(output_path) or\
                not os.path.isfile(output_path),\
                "ERROR: {} exists and is not a file".format(
                    output_path)
            if not os.path.exists(output_path):
                os.makedirs(output_path)
            assert os.path.exists(output_path),\
                "ERROR: Create {} failed".format(output_path)

            for page in os.listdir(issue_dir):
                page_path = os.path.join(issue_dir, page)
                if os.path.isdir(page_path):
                    print("WARN: unexpected directory: {}".format(page))
                    continue
                num_files += 1
                if os.path.splitext(page)[1].lower() != ".xml":
                    non_xml += 1
                    print("WARN: file with no .xml suffic: {}".format(page))
                    continue
                try:
                    document_tree = get_xml(page_path)
                except Exception as e:
                    bad_xml += 1
                    print("WARN: problematic file {}: {}".format(
                        page, str(e)))
                    continue
                metadata = get_xml_metadata(document_tree)
                if metadata[XML_ROOT] == ALTO_ROOT:
                    # alto files are accessed via mets.
                    skipped_alto += 1
                    continue
                if query_xml(document_tree, BLN_PAGE_XPATH):
                    # BL_page files contain layout not text.
                    skipped_bl_page += 1
                    continue
                input_filename = os.path.basename(page)
                input_sub_path = os.path.join(publication, year, issue)
                if metadata[XML_ROOT] == METS_ROOT:
                    mets_match = re.findall(RE_METS, input_filename)
                    output_document_stub = mets_match[0][0]
                else:
                    output_document_stub = os.path.splitext(input_filename)[0]
                output_document_path = os.path.join(output_path,
                                                    output_document_stub)
                try:
                    xslt(document_tree,
                         input_path=etree.XSLT.strparam(issue_dir),
                         input_sub_path=etree.XSLT.strparam(
                             input_sub_path),
                         input_filename=etree.XSLT.strparam(input_filename),
                         output_document_stub=etree.XSLT.strparam(
                             output_document_stub),
                         output_path=etree.XSLT.strparam(
                             output_document_path))
                    converted_ok += 1
                    print("INFO: {} gave XSLT output".format(page_path))
                except Exception as e:
                    converted_bad += 1
                    print("ERROR: {} failed to give XSLT output: {}".format(
                        page, str(e)), file=sys.stderr)
                    continue
            summary = {}
            summary["num_files"] = num_files
            summary["bad_xml"] = bad_xml
            summary["converted_ok"] = converted_ok
            summary["converted_bad"] = converted_bad
            summary["skipped_alto"] = skipped_alto
            summary["skipped_bl_page"] = skipped_bl_page
            summary["non_xml"] = non_xml
            check_convert = num_files - skipped_alto - skipped_bl_page
            if (converted_ok > 0) and (converted_ok == check_convert):
                print("INFO: {} {}".format(issue_dir, str(summary)))
            else:
                print("WARN: {} {}".format(issue_dir, str(summary)))


def check_parameters(publication_dir,
                     txt_out_dir,
                     xslt_file,
                     downsample):
    """
    Check parameters. The following checks are done:

    * publication_dir exists and is a directory.
    * txt_out_dir either does not exists or exists and is a directory.
    * publication_dir and txt_out_dir are not the same directory.
    * xslt_file exists and is a file.
    * downsample is a positive integer.

    :param publication_dir: Publication directory with XML
    :type publication_dir: str or unicode
    :param txt_out_dir: Output directory with plaintext
    :type txt_out_dir: str or unicode
    :param xslt_file: XSLT file to convert XML to plaintext
    :type xslt_file: str or unicode
    :param downsample: Downsample
    :type downsample: int
    :raise AssertionError: if any check fails
    """
    assert downsample > 0, "downsample must be a positive integer"
    assert os.path.exists(publication_dir),\
        "publication_dir, {}, not found".format(publication_dir)
    assert os.path.isdir(publication_dir),\
        "publication_dir, {}, is not a directory".format(publication_dir)
    assert not os.path.isfile(txt_out_dir),\
        "txt_out_dir, {}, is not a directory".format(txt_out_dir)
    assert os.path.normpath(publication_dir) !=\
        os.path.normpath(txt_out_dir),\
        "publication_dir and txt_out_dir, {}, should be different directories".format(publication_dir)
    assert os.path.exists(xslt_file),\
        "xslt_file {} not found".format(xslt_file)
    assert os.path.isfile(xslt_file),\
        "xslt_file {} is not a file".format(xslt_file)
