from hyko_sdk.models import Tag

from hyko_toolkit.node_group import NodeGroup

from .image_converter.metadata import node as image_converter_node
from .markdown_to_pdf.metadata import node as markdown_to_pdf_node
from .ocr_pdf_to_text.metadata import node as ocr_pdf_to_text_node
from .pdf_to_text.metadata import node as pdf_to_text_node
from .video_converter.metadata import node as video_converter_node
from .video_to_audio.metadata import node as video_to_audio_node

node = NodeGroup(
    name="converters",
    description="convert anything to anything.",
    icon="io",
    tag=Tag.utilities,
    nodes=[
        image_converter_node,
        markdown_to_pdf_node,
        ocr_pdf_to_text_node,
        pdf_to_text_node,
        video_converter_node,
        video_to_audio_node,
    ],
)
