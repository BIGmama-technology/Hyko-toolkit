from enum import Enum
from typing import Any

from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.models import CoreModel, MetaDataBase, Tag
from hyko_sdk.utils import field

from ..audio.metadata import input_node as audio_node
from ..image.metadata import input_node as image_node
from ..list.number_metadata import input_node as list_number_node
from ..list.text_metadata import input_node as list_text_node
from ..number.metadata import input_node as number_node
from ..pdf.metadata import input_node as pdf_node
from ..text.metadata import input_node as text_node
from ..video.metadata import input_node as video_node

input_node = ToolkitNode(
    name="Input",
    description="This is an input node",
    tag=Tag.core,
    icon="io",
)


class InputTypes(str, Enum):
    text = "text"
    number = "number"
    image = "image"
    video = "video"
    audio = "audio"
    pdf = "pdf"
    list_of_text = "list_of_text"
    list_of_numbers = "list_of_numbers"


@input_node.set_param
class Params(CoreModel):
    input_type: InputTypes = field(
        description="Type of the input node, when this changes it updates the output port to correspond to it.",
    )


@input_node.callback(trigger="input_type", id="change_input_type")
async def change_input_type(metadata: MetaDataBase, *_: Any):
    input_type = metadata.params["input_type"].value
    metadata.params = {}
    match input_type:
        case InputTypes.text.value:
            return text_node.get_metadata()
        case InputTypes.number.value:
            return number_node.get_metadata()
        case InputTypes.image.value:
            return image_node.get_metadata()
        case InputTypes.video.value:
            return video_node.get_metadata()
        case InputTypes.audio.value:
            return audio_node.get_metadata()
        case InputTypes.pdf.value:
            return pdf_node.get_metadata()
        case InputTypes.list_of_text.value:
            return list_text_node.get_metadata()
        case InputTypes.list_of_numbers.value:
            return list_number_node.get_metadata()
        case _:
            return metadata
