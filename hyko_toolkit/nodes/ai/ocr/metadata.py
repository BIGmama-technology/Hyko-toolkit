from hyko_sdk.models import Tag

from hyko_toolkit.node_group import NodeGroup

from .easyocr.metadata import node as easyocr_node
from .surya_ocr.metadata import node as surya_ocr_node
from .tesseract_ocr.metadata import node as tesseract_ocr_node

node = NodeGroup(
    name="OCR",
    description="OCR models for images and pdfs.",
    icon="pdf",
    tag=Tag.ai,
    nodes=[easyocr_node, surya_ocr_node, tesseract_ocr_node],
)
