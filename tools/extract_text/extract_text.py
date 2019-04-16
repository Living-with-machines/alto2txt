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

The following XSLT files need to be in the current directory:

* extract_text_mets18.xslt: METS 1.8 XSL file.
* extract_text_mets13.xslt: METS 1.3 XSL file.
* extract_text_bln.xslt: BLN XSL file.
* extract_text_ukp.xslt: UKP XSL file.
"""

from __future__ import print_function
import os
import os.path
import re
import sys
from lxml import etree

METS_18_XSLT_FILENAME = "extract_text_mets18.xslt"
""" METS 1.8 XSL filename """
METS_13_XSLT_FILENAME = "extract_text_mets13.xslt"
""" METS 1.3 XSL filename """
BLN_XSLT_FILENAME = "extract_text_bln.xslt"
""" BLN XSL filename """
UKP_XSLT_FILENAME = "extract_text_ukp.xslt"
""" UKP XSL filename """

METS_18_XSLT = "METS1.8"
""" METS 1.8 XSLT ID """
METS_13_XSLT = "METS1.3"
""" METS 1.3 XSLT ID """
BLN_XSLT = "BLN"
""" BLN XSLT ID """
UKP_XSLT = "UKP"
""" UKP XSLT ID """

XSI_NS = "http://www.w3.org/2001/XMLSchema-instance"
""" XML Schema Instance namespace """
SCHEMA_LOCATION = etree.QName(XSI_NS, "schemaLocation")
""" schemaLocation element """
NO_NS_SCHEMA_LOCATION = etree.QName(XSI_NS,
                                    "noNamespaceSchemaLocation")
""" noNamespaceSchemaLocation element """

METS_NS = "http://www.loc.gov/METS/"
""" METS namespace """
METS_18_URI = "http://www.loc.gov/standards/mets/version18/mets.xsd"
""" METS 1.8 schemaLocation """
METS_13_URI = "http://schema.ccs-gmbh.com/docworks/mets-metae.xsd"
""" METS 1.3 schemaLocation """
METS_ROOT = etree.QName(METS_NS, "mets")
""" METS root element """
ALTO_ROOT = "alto"
""" ALTO root element """
BLN_ROOT = "BL_newspaper"
""" BLN root element """
BLN_PAGE_XPATH = "/BL_newspaper/BL_page"
""" XPath for BLN BL_page element """
UKP_NS = "http://tempuri.org/ncbpissue"
""" UKP namespace """
UKP_ROOT = etree.QName(UKP_NS, "UKP")
""" UKP root element """

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


def load_xslts():
    """
    Loads XSLTs and returns in a dictionary.

    The following XSLT files need to be in the current directory:

    * extract_text_mets18.xslt: METS 1.8 XSL file.
    * extract_text_mets13.xslt: METS 1.3 XSL file.
    * extract_text_bln.xslt: BLN XSL file.
    * extract_text_ukp.xslt: BLN UKP file.

    The dictionary keys are: "METS1.8", "METS1.3", "BLN", "UKP".

    :return: XSLTs
    :rtype: dict(str: lxml.etree.XSLT)
    """
    xslts = {}
    xslts[METS_18_XSLT] = etree.XSLT(etree.parse(METS_18_XSLT_FILENAME))
    xslts[METS_13_XSLT] = etree.XSLT(etree.parse(METS_13_XSLT_FILENAME))
    xslts[BLN_XSLT] = etree.XSLT(etree.parse(BLN_XSLT_FILENAME))
    xslts[UKP_XSLT] = etree.XSLT(etree.parse(UKP_XSLT_FILENAME))
    return xslts


def get_xml(filename):
    """
    Gets XML document tree from file.

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
    Extracts information (root element, namespaces, schema locations,
    default schema location) from XML document tree. Returns dict of
    form:

        {
            doctype: <DOCTYPE>,
            namespaces: {<TAG>: <URL>, <TAG>: <URL>, ...},
            no_ns_schema_location: <URL> | None,
            root: <ROOT_ELEMENT>,
            schema_locations: {<URL>: <URL>, ...}
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
        # Convert schema_locations from "namespaceURI schemaURI ..."
        # to dictionary with namespaceURI:schemaURI
        uris = schema_locations.split(" ")
        schema_locations = {uris[i]: uris[i+1]
                            for i in range(0, len(uris), 2)}
    else:
        schema_locations = {}
    metadata = {}
    metadata[XML_ROOT] = root_element_tag
    metadata[XML_DOCTYPE] = doctype
    metadata[XML_NS] = namespaces
    metadata[XML_NO_NS_SCHEMA_LOCATION] = no_ns_schema_location
    metadata[XML_SCHEMA_LOCATIONS] = schema_locations
    return metadata


def query_xml(document_tree, query):
    """
    Runs XPath query and returns results.

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
    print("INFO: processing issue: {}".format(os.path.join(year, issue)))
    summary = {}
    summary["num_files"] = 0
    summary["bad_xml"] = 0
    summary["converted_ok"] = 0
    summary["converted_bad"] = 0
    summary["skipped_alto"] = 0
    summary["skipped_bl_page"] = 0
    summary["skipped_mets_unknown"] = 0
    summary["non_xml"] = 0
    issue_out_dir = os.path.join(txt_out_dir, year, issue)
    assert not os.path.exists(issue_out_dir) or\
        not os.path.isfile(issue_out_dir),\
        "ERROR: {} exists and is not a file".format(issue_out_dir)
    if not os.path.exists(issue_out_dir):
        os.makedirs(issue_out_dir)
    assert os.path.exists(issue_out_dir),\
        "ERROR: Create {} failed".format(issue_out_dir)
    for xml_file in os.listdir(issue_dir):
        xml_file_path = os.path.join(issue_dir, xml_file)
        if os.path.isdir(xml_file_path):
            print("WARN: unexpected directory: {}".format(xml_file))
            continue
        summary["num_files"] += 1
        if os.path.splitext(xml_file)[1].lower() != ".xml":
            summary["non_xml"] += 1
            print("WARN: file with no .xml suffix: {}".format(xml_file))
            continue
        try:
            document_tree = get_xml(xml_file_path)
        except Exception as e:
            summary["bad_xml"] += 1
            print("WARN: problematic file {}: {}".format(xml_file, str(e)))
            continue
        metadata = get_xml_metadata(document_tree)
        if metadata[XML_ROOT] == ALTO_ROOT:
            # alto files are accessed via mets file.
            summary["skipped_alto"] += 1
            continue
        if query_xml(document_tree, BLN_PAGE_XPATH):
            # BL_page files contain layout not text.
            summary["skipped_bl_page"] += 1
            continue
        if metadata[XML_ROOT] == BLN_ROOT:
            xslt = xslts[BLN_XSLT]
        elif metadata[XML_ROOT] == UKP_ROOT:
            xslt = xslts[UKP_XSLT]
        else:
            mets_uri = metadata[XML_SCHEMA_LOCATIONS][METS_NS]
            if mets_uri == METS_18_URI:
                xslt = xslts[METS_18_XSLT]
            elif mets_uri == METS_13_URI:
                xslt = xslts[METS_13_XSLT]
            else:
                # Unknown METS.
                print("WARN: unknown METS schema {}: {}".format(
                    xml_file,
                    mets_uri))
                summary["skipped_mets_unknown"] += 1
                continue
        input_filename = os.path.basename(xml_file)
        input_sub_path = os.path.join(publication, year, issue)
        if metadata[XML_ROOT] == METS_ROOT:
            mets_match = re.findall(RE_METS, input_filename)
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
            print("INFO: {} gave XSLT output".format(xml_file_path))
        except Exception as e:
            summary["converted_bad"] += 1
            print("ERROR: {} failed to give XSLT output: {}".format(
                xml_file, str(e)), file=sys.stderr)
            continue
    if (summary["converted_ok"] > 0) and\
       (summary["converted_ok"] == (summary["num_files"] -
                                    summary["skipped_alto"] -
                                    summary["skipped_mets_unknown"] -
                                    summary["skipped_bl_page"])):
        print("INFO: {} {}".format(issue_dir, str(summary)))
    else:
        print("WARN: {} {}".format(issue_dir, str(summary)))


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
                print("WARN: unexpected file: {}".format(
                    os.path.join(year, issue)))
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
                         xslts,
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
    :param xslts: XSLTs to convert XML to plaintext
    :type xslts: dict(str: lxml.etree.XSLT)
    :param downsample: Downsample, converting every Nth issue only
    :type downsample: int
    """
    print("INFO: processing: {}".format(publications_dir))
    for publication in os.listdir(publications_dir):
        publication_dir = os.path.join(publications_dir, publication)
        if not os.path.isdir(publication_dir):
            print("WARN: unexpected file: {}".format(publication_dir))
            continue
        publication_txt_out_dir = os.path.join(txt_out_dir, publication)
        publication_to_text(publication_dir,
                            publication_txt_out_dir,
                            xslts,
                            downsample)


def check_parameters(xml_in_dir, txt_out_dir, downsample):
    """
    Check parameters. The following checks are done:

    * xml_in_dir exists and is a directory.
    * txt_out_dir either does not exists or exists and is a directory.
    * xml_in_dir and txt_out_dir are not the same directory.
    * downsample is a positive integer.

    :param xml_in_dir: Input directory with XML publications
    :type xml_in_dir: str or unicode
    :param txt_out_dir: Output directory for plaintext articles
    :type txt_out_dir: str or unicode
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


def xml_publications_to_text(xml_in_dir,
                             txt_out_dir,
                             is_singleton=False,
                             downsample=1):
    """
    Converts XML publications to plaintext articles and generates
    minimal metadata.

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
    :param downsample: Downsample, converting every Nth issue only
    :type downsample: int
    :param is_singleton: xml_in_dir holds XML for a single publication
    (True) or multiple publications (False)
    :type is_singleton: bool
    :raise AssertionError: if any parameter check fails (see
    check_parameters)
    """
    check_parameters(xml_in_dir, txt_out_dir, downsample)
    xslts = load_xslts()
    if is_singleton:
        publication_to_text(xml_in_dir,
                            txt_out_dir,
                            xslts,
                            downsample)
    else:
        publications_to_text(xml_in_dir,
                             txt_out_dir,
                             xslts,
                             downsample)
