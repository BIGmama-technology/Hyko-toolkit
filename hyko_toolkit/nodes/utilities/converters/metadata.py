from enum import Enum
from typing import Any

from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.models import CoreModel, MetaDataBase, Tag
from hyko_sdk.utils import field

from .image_converter.metadata import func as image_converter_node
from .markdown_to_pdf.metadata import func as markdown_to_pdf_node
from .ocr_pdf_to_text.metadata import func as ocr_pdf_to_text_node
from .pdf_to_text.metadata import func as pdf_to_text_node
from .video_converter.metadata import func as video_converter_node
from .video_to_audio.metadata import func as video_to_audio_node

node = ToolkitNode(
    name="converters",
    description="convert anything to anything.",
    icon="io",
    tag=Tag.utilities,
)


class Converters(str, Enum):
    image_converter = "image_converter"
    markdown_to_pdf = "markdown_to_pdf"
    ocr_pdf_to_text = "ocr_pdf_to_text"
    video_converter = "video_converter"
    video_to_audio = "video_to_audio"
    pdf_to_text = "pdf_to_text"


@node.set_param
class Params(CoreModel):
    converter: Converters = field(
        description="Type of the input node, when this changes it updates the output port to correspond to it.",
    )


@node.callback(trigger="converter", id="change_converter")
async def change_converter_type(metadata: MetaDataBase, *_: Any):
    converter = metadata.params["converter"].value
    metadata.params = {}
    match converter:
        case Converters.image_converter.value:
            return image_converter_node.get_metadata()
        case Converters.markdown_to_pdf.value:
            return markdown_to_pdf_node.get_metadata()
        case Converters.ocr_pdf_to_text.value:
            return ocr_pdf_to_text_node.get_metadata()
        case Converters.pdf_to_text.value:
            return pdf_to_text_node.get_metadata()
        case Converters.video_converter.value:
            return video_converter_node.get_metadata()
        case Converters.video_to_audio.value:
            return video_to_audio_node.get_metadata()
        case _:
            return metadata
