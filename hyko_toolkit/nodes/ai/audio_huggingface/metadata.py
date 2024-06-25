from hyko_sdk.models import Tag

from hyko_toolkit.node_group import NodeGroup

from .speech_to_text.metadata import node as speech_to_text_node
from .text_to_speech.metadata import node as text_to_speech_node

node = NodeGroup(
    name="Huggingface audio models",
    description="Huggingface computer vision models.",
    icon="hf",
    tag=Tag.ai,
    nodes=[speech_to_text_node, text_to_speech_node],
)
