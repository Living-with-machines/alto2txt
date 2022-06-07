"""
XML utilities.
"""

import os
from lxml import etree
from alto2txt import xslts


METS_18_XSLT = "extract_text_mets18.xslt"
""" METS 1.8 XSLT """
METS_13_XSLT = "extract_text_mets13.xslt"
""" METS 1.3 XSLT """
BLN_XSLT = "extract_text_bln.xslt"
""" BLN XSLT """
UKP_XSLT = "extract_text_ukp.xslt"
""" UKP XSLT """

XSI_NS = "http://www.w3.org/2001/XMLSchema-instance"
""" XML Schema Instance namespace """
SCHEMA_LOCATION = etree.QName(XSI_NS, "schemaLocation")
""" schemaLocation element """
NO_NS_SCHEMA_LOCATION = etree.QName(XSI_NS, "noNamespaceSchemaLocation")
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

LWM_NS = {"ukp": UKP_NS, "mets": METS_NS}
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


def get_path(module, *name):
    """
    Gets path to file in module, given module and relative path.

    :param module: module
    :type module: module
    :param *name: file name components
    :type *name: str
    :return: path to file
    :rtype: str
    """
    return os.path.join(os.path.dirname(module.__file__), *name)


def load_xslts():
    """
    Loads XSLTs and returns in a dictionary.

    The following XSLT files need to be in an extract_text.xslts
    module:

    * extract_text_mets18.xslt: METS 1.8 XSL file.
    * extract_text_mets13.xslt: METS 1.3 XSL file.
    * extract_text_bln.xslt: BLN XSL file.
    * extract_text_ukp.xslt: BLN UKP file.

    :return: XSLTs
    :rtype: dict(str: lxml.etree.XSLT)
    """
    xsl_transforms = {}
    for xslt_name in [METS_18_XSLT, METS_13_XSLT, BLN_XSLT, UKP_XSLT]:
        xslt_file = get_path(xslts, xslt_name)
        xsl_transforms[xslt_name] = etree.XSLT(etree.parse(xslt_file))
    return xsl_transforms


def get_xml(filename):
    """
    Gets XML document tree from file.

    :param filename: XML filename
    :type filename: str
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
        schema_locations = {uris[i]: uris[i + 1] for i in range(0, len(uris), 2)}
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
    :type query: str
    :return: Query results
    :rtype: Query-specific
    """
    root_element = document_tree.getroot()
    result = root_element.xpath(query, namespaces=LWM_NS)
    return result
