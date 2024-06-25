from hyko_sdk.models import Tag

from hyko_toolkit.node_group import NodeGroup

from .depth_estimation.metadata import node as depth_estimation_node
from .image_classification.metadata import node as hf_image_classification_node
from .image_segmentation.metadata import node as image_segmentation_node
from .mask_generation.metadata import node as mask_generation_node
from .object_detection.metadata import node as hf_object_detection_node
from .video_classification.metadata import node as video_classification_node
from .zero_shot_image_classification.metadata import (
    node as zero_shot_image_classification_node,
)

node = NodeGroup(
    name="Computer Vision Hugging Face models",
    description="Hugging Face computer vision models.",
    icon="hf",
    tag=Tag.ai,
    nodes=[
        depth_estimation_node,
        hf_image_classification_node,
        image_segmentation_node,
        mask_generation_node,
        hf_object_detection_node,
        video_classification_node,
        zero_shot_image_classification_node,
    ],
)
