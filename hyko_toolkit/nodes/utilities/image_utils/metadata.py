from hyko_sdk.models import Tag

from hyko_toolkit.node_group import NodeGroup

from .brightness_and_contrast.metadata import func as brightness_and_contrast_node
from .crop_border.metadata import func as crop_border_node
from .crop_edges.metadata import func as crop_edges_node
from .flip.metadata import func as flip_node
from .get_dimensions.metadata import func as get_dimensions_node
from .opacity.metadata import func as opacity_node
from .padding.metadata import func as padding_node
from .resize_factor.metadata import func as resize_factor_node
from .resize_resolution.metadata import func as resize_resolution_node
from .rotate.metadata import func as rotate_node
from .stack_images.metadata import func as stack_images_node

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
