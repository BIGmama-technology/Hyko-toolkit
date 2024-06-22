import zipfile
from xml.etree.ElementTree import XML

"""
Module that extract text from MS XML Word document (.docx).
(Inspired by python-docx <https://github.com/mikemaccana/python-docx>)
"""

WORD_NAMESPACE = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
PARA = WORD_NAMESPACE + "p"
TEXT = WORD_NAMESPACE + "t"


def get_docx_text(path: str):
    """
    Take the path of a docx file as argument, return the text in unicode.
    """
    document = zipfile.ZipFile(path)
    xml_content = document.read("word/document.xml")
    document.close()
    tree = XML(xml_content)

    text = "\n\n".join(list(tree.itertext()))

    return text
