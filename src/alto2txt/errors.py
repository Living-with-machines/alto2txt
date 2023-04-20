class XMLError:
    UNKNOWN_SCHEMA = "Unknown XML schema"
    XML_SYNTAX_ERROR = "XML Syntax Error"
    UNKNOWN_ROOT = "Unknown root"
    CONVERTED_BAD = "XML file failed to give XSLT output"

    errors = [UNKNOWN_SCHEMA, XML_SYNTAX_ERROR, UNKNOWN_ROOT, CONVERTED_BAD]

    def __init__(self, error=None, file=None, schema=None):
        self.file = file
        self.schema = schema

    def write(self):
        if self.file and self.schema:
            print(f"{self.error}: {self.file} ({self.schema})")
            return

        if self.file:
            print(f"{self.error}: {self.file}")
            return

        print(f"{self.error}")
        return
