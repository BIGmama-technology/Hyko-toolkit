from hyko_sdk.models import Tag

from hyko_toolkit.node_group import NodeGroup

from .image_restoration.metadata import node as image_restoration_node
from .text_to_video.metadata import node as text_to_video_node
from .transcribe_speech.metadata import node as transcribe_speech_node
from .upscale_images.metadata import node as upscale_images_node
from .vision_models.metadata import node as vision_models_node

node = NodeGroup(
    name="Replicate APIs",
    description="user Replicate AI models.",
    icon="replicate",
    tag=Tag.ai,
    nodes=[
        image_restoration_node,
        text_to_video_node,
        transcribe_speech_node,
        upscale_images_node,
        vision_models_node,
    ],
)
