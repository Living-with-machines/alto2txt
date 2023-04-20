"""
Functions to convert XML (in METS 1.8/ALTO 1.4, METS 1.3/ALTO 1.4, BLN
or UKP format) publications to plaintext articles and generate minimal
metadata.
"""

import logging
import os
import os.path
import re
from pathlib import Path
from typing import List, Optional, Union

from lxml import etree

from . import xml
from .errors import XMLError

logger = logging.getLogger(__name__)
""" Module-level logger. """


# SUGGESTION:
# Alternative function to essentially take the place of issue_to_text()
# but with the loop over METS files taking place in the calling function.
def xml_to_text(
    mets_path: str,
    input_dir: str,
    output_dir: str,
    xslts: dict,
    in_zip: Optional[str] = None,
) -> Union[bool, str]:
    """
    Transform an XML file to text using an XSLT transformation.

    :param mets_path: The path to the XML file to be transformed.
    :type mets_path: str
    :param input_dir: The input directory containing the XML file.
    :type input_dir: str
    :param output_dir : The output directory where the transformed file will be saved.
    :type output_dir : str
    :param xslts : A dictionary containing XSLT files.
    :type xslts : dict
    :return: True if transformation was successful, otherwise returns a string error message.
    :rtype: Union[bool, str]
    """

    # Get METS tree
    #     def get_xml_from_string(string):
    #         parser = etree.XMLParser()
    #         document_tree = etree.parse(io.BytesIO(string))
    #         return document_tree
    #     if is_zipfile(input_dir):
    #         zf = ZipFile(input_dir, 'r')

    #         with zf.open(str(mets_path)) as xml_f:
    #             contents = xml_f.read()
    #             # contents = contents.decode("utf-8")
    #             try:
    #                 document_tree = get_xml_from_string(contents)
    #             except etree.XMLSyntaxError:
    #                 logger.warning(f"Problematic file {mets_path}: {e}")
    #                 return XMLError(error=XMLError.XML_SYNTAX_ERROR, file=mets_path)
    #     else:
    try:
        document_tree = xml.get_xml(mets_path)
    except etree.XMLSyntaxError:
        logger.warning(f"Problematic file {mets_path}: {e}")
        return XMLError(error=XMLError.XML_SYNTAX_ERROR, file=mets_path)

    # Get metadata from METS tree
    metadata = xml.get_xml_metadata(document_tree)

    # Set up variables passed to XSLT
    input_filename = mets_path.name
    input_path = mets_path.parent.resolve()
    input_sub_path = str(mets_path.parent).replace(input_dir, "")
    output_document_stub = str(input_filename).replace("_mets.xml", "")

    if input_sub_path.startswith("/"):
        input_sub_path = input_sub_path.lstrip("/")

    # Create output path
    output_path = str(
        Path(output_dir).resolve() / input_sub_path / output_document_stub
    )

    # Set up xslt for correct XML schema
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
            logger.warning("Unknown METS schema {mets_path}: {mets_uri}")
            return XMLError(
                error=XMLError.UNKNOWN_SCHEMA, file=mets_path, schema=mets_uri
            )
    else:
        return XMLError(error=XMLError.UNKNOWN_ROOT, file=mets_path)

    # Set up XSLT parameters
    xslt_params = {
        "input_dir": input_dir,
        "input_path": input_path,
        "input_sub_path": input_sub_path,
        "input_filename": input_filename,
        "output_document_stub": output_document_stub,
        "output_path": output_path,
    }

    # Ensure correct XSLT parameter types
    xslt_params = {
        x: etree.XSLT.strparam(str(y)) for x, y in xslt_params.items()
    }

    # Ensure output path exists
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    # Run XSLT
    try:
        xslt(document_tree, **xslt_params)
        logger.info(f"{mets_path} gave XSLT output")
    except Exception as e:
        logger.error(f"{mets_path} failed to give XSLT output: {e}")
        return XMLError(error=XMLError.CONVERTED_BAD, file=mets_path)

    return True


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
    assert os.path.exists(issue_out_dir), "Create {} failed".format(
        issue_out_dir
    )
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
                logger.warning(
                    "Unknown METS schema %s: %s", xml_file, mets_uri
                )
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
                logger.warning(
                    "Unexpected file: %s", os.path.join(year, issue)
                )
                continue
            # Only process every Nth issue (when using downsample).
            issue_counter += 1
            if (issue_counter % downsample) != 0:
                continue
            issue_to_text(
                publication, year, issue, issue_dir, txt_out_dir, xslts
            )


def process_mets_files_in_directory(
    input_dir: str,
    output_dir: str,
    xslts: dict,
    downsample: int = 1,
) -> dict:
    """
    Process METS files in a specified input directory.

    ..
        Note: This function replaces publications_to_text below.

    :param input_dir: Path to the input directory containing METS files.
    :type input_dir: str, optional
    :param output_dir: Path to the output directory for the processed files.
    :type output_dir: str, optional
    :param downsample: Amount to downsample the number of files processed, by default 1
    :type downsample: int, optional
    :param xslts: A dictionary containing XSLT files.
    :type xslts: dict
    :return: A dictionary containing a report of successful files, and any errors that
        occurred.
    :rtype: dict
    """

    def setup_summary() -> dict:
        """Private function that sets up a dictionary for reporting"""
        summary = {error: 0 for error in XMLError.errors}
        summary["num_files"] = 0
        return summary

    def get_mets_files(input_dir: str, downsample: int) -> List[str]:
        """
        Private function that gets a list of METS XML files in the given directory.

        :param input_dir: The directory where the METS files are located.
        :type input_dir: str
        :param downsample: A factor to downsample the list of METS files.
        :type downsample: int
        :return: A list of paths to the METS XML files.
        :rtype: List[str]
        """
        #   if is_zipfile(input_dir):
        #       archive = ZipFile(input_dir, "r")
        #       files = archive.namelist()
        #   else:
        files = Path(input_dir).glob("**/*_mets.xml")

        lst = [Path(f) for f in list(files) if str(f).endswith("_mets.xml")]
        return [f for ix, f in enumerate(lst) if not (ix % downsample) != 0]

    def check_for_unexpected_files(
        input_dir: str, downsample: int = 1
    ) -> None:
        """
        Private function that checks for unexpected files in an input directory,
        optionally downsampled.
        """
        mets_files_unexpected_dirs = [
            mets_file
            for mets_file in get_mets_files(input_dir, downsample)
            if mets_file.is_dir()
        ]
        if len(mets_files_unexpected_dirs):
            print("Warning: encountered METS XML paths that are directories.")
            print("- " + mets_files_unexpected_dirs.join("\n- "))

    # Expand the input dir
    input_dir = str(Path(input_dir).resolve())

    # Make sure there are no strange files in the input directory. If there are, warn!
    check_for_unexpected_files(input_dir, downsample)

    # Get a proper list of METS files
    mets_files_for_processing = [
        mets_file
        for mets_file in get_mets_files(input_dir, downsample)
        if not mets_file.is_dir()
    ]

    # Now, do something to each proper METS file:
    summary = setup_summary()
    for mets_path in mets_files_for_processing:
        logger.info(f"Processing {mets_path.name}...")
        result = xml_to_text(mets_path, input_dir, output_dir, xslts)

        if isinstance(result, XMLError):
            result.write()
            summary[XMLError.error] += 1
        else:
            summary["num_files"] += 1

    return summary


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
        publication_to_text(
            publication_dir, publication_txt_out_dir, xslts, downsample
        )
