from hyko_sdk.models import Tag

from hyko_toolkit.node_group import NodeGroup

from ..llms.metadata import openai_llm as openai_llm_node
from .speech_to_text.metadata import node as openai_speech_to_text_node
from .text_to_speech.metadata import node as openai_text_to_speech_node
from .vision.metadata import node as openai_vision_node

node = NodeGroup(
    name="Openai",
    description="Group node for all openai models: gpt-4, text to speech, speech to text...",
    icon="openai",
    tag=Tag.ai,
    nodes=[
        openai_speech_to_text_node,
        openai_text_to_speech_node,
        openai_vision_node,
        openai_llm_node,
    ],
)
