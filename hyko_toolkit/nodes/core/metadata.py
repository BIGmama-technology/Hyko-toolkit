from hyko_sdk.models import Tag

from hyko_toolkit.node_group import NodeGroup

from .audio.metadata import input_node as audio_node
from .audio.metadata import output_node as audio_node_output
from .document.metadata import input_node as table_node
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

output_node = NodeGroup(
    name="Output",
    description="This is an output node",
    icon="io",
    tag=Tag.core,
    nodes=[
        audio_node_output,
        image_node_output,
        list_number_node_output,
        list_text_node_output,
        number_node_output,
        pdf_node_output,
        text_node_output,
        video_node_output,
    ],
)

input_node = NodeGroup(
    name="Input",
    description="This is an input node",
    icon="io",
    tag=Tag.core,
    nodes=[
        audio_node,
        image_node,
        list_number_node,
        list_text_node,
        number_node,
        pdf_node,
        text_node,
        video_node,
        table_node,
    ],
)
