from hyko_sdk.models import Tag

from hyko_toolkit.node_group import NodeGroup

from .image_to_image_with_a_mask.metadata import node as image_to_image_with_a_mask_node
from .image_to_image_with_prompt.metadata import node as image_to_image_with_prompt_node
from .image_to_video.metadata import node as stability_image_to_video_node
from .image_upscaler.metadata import node as image_upscaler_node
from .text_to_image.metadata import node as text_to_image_node

node = NodeGroup(
    name="Stability AI APIs",
    description="Stability AI models.",
    icon="stabilityai",
    tag=Tag.ai,
    nodes=[
        image_to_image_with_a_mask_node,
        image_to_image_with_prompt_node,
        stability_image_to_video_node,
        image_upscaler_node,
        text_to_image_node,
    ],
)
