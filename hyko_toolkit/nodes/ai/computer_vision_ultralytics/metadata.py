from hyko_sdk.models import Tag

from hyko_toolkit.node_group import NodeGroup

from .image_classification.metadata import node as image_classification_node
from .image_instance_segmentation.metadata import (
    node as image_instance_segmentation_node,
)
from .image_obb_object_detection.metadata import node as image_obb_object_detection_node
from .image_object_detection.metadata import node as image_object_detection_node
from .image_pose_estimation.metadata import node as image_pose_estimation_node
from .video_instance_segmentation.metadata import (
    node as video_instance_segmentation_node,
)
from .video_obb_object_detection.metadata import node as video_obb_object_detection_node
from .video_object_detection.metadata import node as video_object_detection_node
from .video_pose_estimation.metadata import node as video_pose_estimation_node

node = NodeGroup(
    name="Computer Vision Ultralytics models",
    description="Ultralytics computer vision models.",
    icon="image",
    tag=Tag.ai,
    nodes=[
        image_classification_node,
        image_instance_segmentation_node,
        image_obb_object_detection_node,
        image_object_detection_node,
        image_pose_estimation_node,
        video_instance_segmentation_node,
        video_obb_object_detection_node,
        video_object_detection_node,
        video_pose_estimation_node,
    ],
)
