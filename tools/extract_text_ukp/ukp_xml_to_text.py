"""
Parse a UKP XML document into 1 plaintext file per "article" element.

Usage:

    python ukp_xml_to_text.py <UKP_FILE>

UKP documents (documents with root element UKP or
{http://tempuri.org/ncbpissue}UKP are found in files with the
following naming scheme:

* BLSD-<YYYY>-MM>-<DD>.xml
* LAGER-<YYYY>-MM>-<DD>.xml

N <ARTICLE>.txt plaintext files are output, one per article, where
<ARTICLE> is the value of the "article/id/text()" for the article.
"""

import sys
from lxml import etree


def ukp_xml_to_text(filename):
    """
    Parse a UKP XML document into 1 plaintext file per "article"
    element.

    :param filename: filename
    :type filename: str or unicode
    """
    with open(filename, "r") as f:
        parser = etree.XMLParser(recover=False)
        document_tree = etree.parse(f, parser)
    root_element = document_tree.getroot()
    # Can't query without knowing namespace of element so adopt hacky
    # approach to extract and use default namespace.
    ns = root_element.nsmap
    default_ns = ns[None]
    query_ns = {"ns": default_ns}
    articles = document_tree.xpath("//ns:article", namespaces=query_ns)
    assert articles, "No'article elements"
    print(("Number of articles: " + str(len(articles))))
    for article in articles:
        article_id = article.xpath("ns:id/text()", namespaces=query_ns)[0]
        print((str(article_id)))
        title = article.xpath(".//ns:text.title//ns:wd/text()",
                              namespaces=query_ns)
        preamble = article.xpath(".//ns:text.preamble//ns:wd/text()",
                                 namespaces=query_ns)
        content = article.xpath(".//ns:text.cr//ns:wd/text()",
                                namespaces=query_ns)
        with open(article_id + ".txt", "w") as f:
            for block in [title, preamble, content]:
                for word in block:
                    # Encode to avert UnicodeEncodeError: 'ascii'
                    # codec can't encode character errors.
                    f.write(word.encode('utf-8'))
                    f.write(" ")
                f.write("\n")


if __name__ == "__main__":
    filename = sys.argv[1]
    ukp_xml_to_text(filename)
