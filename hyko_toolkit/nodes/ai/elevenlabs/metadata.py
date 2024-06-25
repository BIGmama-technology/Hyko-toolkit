from hyko_sdk.models import Tag

from hyko_toolkit.node_group import NodeGroup

from .speech_to_speech.metadata import node as elevenlabs_speech_to_speech
from .text_to_speech.metadata import node as elevenlabs_text_to_speech

node = NodeGroup(
    name="Elevenlabs",
    description="Group node for all elevenlabs models: text to speech, speech to speech...",
    icon="models",
    tag=Tag.ai,
    nodes=[elevenlabs_text_to_speech, elevenlabs_speech_to_speech],
)
