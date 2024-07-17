from hyko_sdk.models import Tag

from hyko_toolkit.node_group import NodeGroup

from .image_converter.metadata import node as image_converter_node
from .video_to_audio.metadata import node as video_to_audio_node

node = NodeGroup(
    name="converters",
    description="convert anything to anything.",
    icon="io",
    tag=Tag.utilities,
    nodes=[
        image_converter_node,
        video_to_audio_node,
    ],
)
