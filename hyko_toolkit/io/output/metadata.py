from enum import Enum
from typing import Any

from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.models import Category, CoreModel, MetaDataBase
from hyko_sdk.utils import field

from ..audio.metadata import output_node as audio_node
from ..image.metadata import output_node as image_node
from ..list.number_metadata import output_node as list_number_node
from ..list.text_metadata import output_node as list_text_node
from ..number.metadata import output_node as number_node
from ..pdf.metadata import output_node as pdf_node
from ..text.metadata import output_node as text_node
from ..video.metadata import output_node as video_node

output_node = ToolkitNode(
    name="Output",
    task="Outputs",
    description="This is an output node",
    category=Category.IO,
    icon="io",
)


class OutputTypes(str, Enum):
    text = "text"
    number = "number"
    image = "image"
    video = "video"
    audio = "audio"
    pdf = "pdf"
    list_of_text = "list_of_text"
    list_of_numbers = "list_of_numbers"


@output_node.set_param
class Params(CoreModel):
    output_type: OutputTypes = field(
        description="Type of the output node, when this changes it updates the input port to correspond to it.",
    )


@output_node.callback(trigger="output_type", id="change_output_type")
async def change_output_type(metadata: MetaDataBase, *_: Any):
    output_type = metadata.params["output_type"].value
    metadata.params = {}
    match output_type:
        case OutputTypes.text.value:
            return text_node.get_metadata()
        case OutputTypes.number.value:
            return number_node.get_metadata()
        case OutputTypes.image.value:
            return image_node.get_metadata()
        case OutputTypes.video.value:
            return video_node.get_metadata()
        case OutputTypes.audio.value:
            return audio_node.get_metadata()
        case OutputTypes.pdf.value:
            return pdf_node.get_metadata()
        case OutputTypes.list_of_text.value:
            return list_text_node.get_metadata()
        case OutputTypes.list_of_numbers.value:
            return list_number_node.get_metadata()
        case _:
            return metadata
