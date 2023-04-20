import logging

logger = logging.getLogger(__name__)
""" Module-level logger. """


class XMLError:
    UNKNOWN_SCHEMA = "Unknown XML schema"
    UNSUPPORTED_SCHEMA = "Unsupported XML schema for operation"
    XML_SYNTAX_ERROR = "XML Syntax Error"
    UNKNOWN_ROOT = "Unknown root"
    CONVERTED_BAD = "XML file failed to give XSLT output"
    NO_DATES = "No dates found"
    TOO_MANY_DATES = "Too many dates found"
    NO_DATE_TEXT = "Date has no text"
    DATE_MALFORMED = "Date is not formatted correctly (YYYY-MM-DD)"
    NO_IDENTIFIERS = "No identifiers found"
    TOO_MANY_IDENTIFIERS = "Too many identifiers found"
    NO_IDENTIFIER_TEXT = "Identifier has no text"
    GENERAL_XSLT_ERROR = "General XSLT Error"
    CANNOT_RESOLVE_URI = "XSLT Error, cannot resolve URI"

    errors = [
        UNKNOWN_SCHEMA,
        UNSUPPORTED_SCHEMA,
        XML_SYNTAX_ERROR,
        UNKNOWN_ROOT,
        CONVERTED_BAD,
        NO_DATES,
        TOO_MANY_DATES,
        NO_DATE_TEXT,
        DATE_MALFORMED,
        NO_IDENTIFIERS,
        TOO_MANY_IDENTIFIERS,
        NO_IDENTIFIER_TEXT,
        GENERAL_XSLT_ERROR,
        CANNOT_RESOLVE_URI,
    ]

    def __init__(self, error=None, file=None, schema=None, log_error=True):
        self.file = file
        self.schema = schema
        self.error = error

        if log_error:
            if file:
                logger.error(f"An XMLError occurred: {self._get_message()}")

    def write(self):
        print(self._get_message())
        return

    def _get_message(self):
        if self.file and self.schema:
            return f"{self.error}: {self.file} ({self.schema})"

        if self.file:
            return f"{self.error}: {self.file}"

        return f"{self.error}"
