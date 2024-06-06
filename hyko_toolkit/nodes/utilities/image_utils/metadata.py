from hyko_sdk.models import Tag

from hyko_toolkit.node_group import NodeGroup

from .brightness_and_contrast.metadata import node as brightness_and_contrast_node
from .crop_border.metadata import node as crop_border_node
from .crop_edges.metadata import node as crop_edges_node
from .flip.metadata import node as flip_node
from .get_dimensions.metadata import node as get_dimensions_node
from .opacity.metadata import node as opacity_node
from .padding.metadata import node as padding_node
from .resize_factor.metadata import node as resize_factor_node
from .resize_resolution.metadata import node as resize_resolution_node
from .rotate.metadata import node as rotate_node
from .stack_images.metadata import node as stack_images_node

node = NodeGroup(
    name="Image utilities",
    description="perform various image processing tasks.",
    icon="image",
    tag=Tag.utilities,
    nodes=[
        brightness_and_contrast_node,
        crop_border_node,
        crop_edges_node,
        flip_node,
        get_dimensions_node,
        opacity_node,
        padding_node,
        resize_factor_node,
        resize_resolution_node,
        rotate_node,
        stack_images_node,
    ],
)
