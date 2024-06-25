from hyko_sdk.models import Tag

from hyko_toolkit.node_group import NodeGroup

from .image_to_text.metadata import node as image_to_text_node
from .text_to_image.metadata import node as text_to_image_node
from .visual_question_answering.metadata import node as visual_question_answering_node

node = NodeGroup(
    name="Multimodal Hugging Face APIs",
    description="Hugging Face multimodal models.",
    icon="hf",
    tag=Tag.ai,
    nodes=[
        image_to_text_node,
        text_to_image_node,
        visual_question_answering_node,
    ],
)
