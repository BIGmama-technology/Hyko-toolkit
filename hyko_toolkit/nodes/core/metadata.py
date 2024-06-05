from enum import Enum
from typing import Any

from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.models import CoreModel, MetaDataBase, Tag
from hyko_sdk.utils import field

from .audio.metadata import input_node as audio_node
from .audio.metadata import output_node as audio_node_output
from .csv.metadata import input_node as csv_node
from .image.metadata import input_node as image_node
from .image.metadata import output_node as image_node_output
from .list.number_metadata import input_node as list_number_node
from .list.number_metadata import output_node as list_number_node_output
from .list.text_metadata import input_node as list_text_node
from .list.text_metadata import output_node as list_text_node_output
from .number.metadata import input_node as number_node
from .number.metadata import output_node as number_node_output
from .pdf.metadata import input_node as pdf_node
from .pdf.metadata import output_node as pdf_node_output
from .text.metadata import input_node as text_node
from .text.metadata import output_node as text_node_output
from .video.metadata import input_node as video_node
from .video.metadata import output_node as video_node_output

output_node = ToolkitNode(
    name="Output",
    description="This is an output node",
    icon="io",
)


class CoreTypes(str, Enum):
    text = "text"
    number = "number"
    image = "image"
    video = "video"
    audio = "audio"
    pdf = "pdf"
    list_of_text = "list_of_text"
    list_of_numbers = "list_of_numbers"
    csv = "csv"


input_node = ToolkitNode(
    name="Input",
    description="This is an input node",
    tag=Tag.core,
    icon="io",
)


@input_node.set_param
class OutputParams(CoreModel):
    input_type: CoreTypes = field(
        description="Type of the input node, when this changes it updates the output port to correspond to it.",
    )


@input_node.callback(trigger="input_type", id="change_input_type")
async def change_input_type(metadata: MetaDataBase, *_: Any):
    input_type = metadata.params["input_type"].value
    metadata.params = {}
    match input_type:
        case CoreTypes.text.value:
            return text_node.get_metadata()
        case CoreTypes.number.value:
            return number_node.get_metadata()
        case CoreTypes.image.value:
            return image_node.get_metadata()
        case CoreTypes.video.value:
            return video_node.get_metadata()
        case CoreTypes.audio.value:
            return audio_node.get_metadata()
        case CoreTypes.pdf.value:
            return pdf_node.get_metadata()
        case CoreTypes.list_of_text.value:
            return list_text_node.get_metadata()
        case CoreTypes.list_of_numbers.value:
            return list_number_node.get_metadata()
        case CoreTypes.csv.value:
            return csv_node.get_metadata()
        case _:
            return metadata


@output_node.set_param
class InputParams(CoreModel):
    output_type: CoreTypes = field(
        description="Type of the output node, when this changes it updates the input port to correspond to it.",
    )


@output_node.callback(trigger="output_type", id="change_output_type")
async def change_output_type(metadata: MetaDataBase, *_: Any):
    output_type = metadata.params["output_type"].value
    metadata.params = {}
    match output_type:
        case CoreTypes.text.value:
            return text_node_output.get_metadata()
        case CoreTypes.number.value:
            return number_node_output.get_metadata()
        case CoreTypes.image.value:
            return image_node_output.get_metadata()
        case CoreTypes.video.value:
            return video_node_output.get_metadata()
        case CoreTypes.audio.value:
            return audio_node_output.get_metadata()
        case CoreTypes.pdf.value:
            return pdf_node_output.get_metadata()
        case CoreTypes.list_of_text.value:
            return list_text_node_output.get_metadata()
        case CoreTypes.list_of_numbers.value:
            return list_number_node_output.get_metadata()
        case _:
            return metadata
