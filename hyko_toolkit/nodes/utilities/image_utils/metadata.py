from enum import Enum
from typing import Any

from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.models import CoreModel, MetaDataBase, Tag
from hyko_sdk.utils import field

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

node = ToolkitNode(
    name="Image utilities",
    description="perform various image processing tasks.",
    icon="image",
    tag=Tag.utilities,
)


class ImageUtils(str, Enum):
    brightness_and_contrast = "brightness_and_contrast"
    crop_border = "crop_border"
    crop_edges = "crop_edges"
    flip = "flip"
    get_dimensions = "get_dimensions"
    opacity = "opacity"
    padding = "padding"
    resize_factor = "resize_factor"
    resize_resolution = "resize_resolution"
    rotate = "rotate"
    stack_images = "stack_images"


@node.set_param
class Params(CoreModel):
    image_util: ImageUtils = field(
        description="Type of the image utility node, when this changes it updates the output port to correspond to it.",
    )


@node.callback(trigger="image_util", id="change_image_util")
async def change_image_util_type(metadata: MetaDataBase, *_: Any):
    image_util = metadata.params["image_util"].value
    metadata.params = {}
    match image_util:
        case ImageUtils.brightness_and_contrast.value:
            return brightness_and_contrast_node.get_metadata()
        case ImageUtils.crop_border.value:
            return crop_border_node.get_metadata()
        case ImageUtils.crop_edges.value:
            return crop_edges_node.get_metadata()
        case ImageUtils.flip.value:
            return flip_node.get_metadata()
        case ImageUtils.get_dimensions.value:
            return get_dimensions_node.get_metadata()
        case ImageUtils.opacity.value:
            return opacity_node.get_metadata()
        case ImageUtils.padding.value:
            return padding_node.get_metadata()
        case ImageUtils.resize_factor.value:
            return resize_factor_node.get_metadata()
        case ImageUtils.resize_resolution.value:
            return resize_resolution_node.get_metadata()
        case ImageUtils.rotate.value:
            return rotate_node.get_metadata()
        case ImageUtils.stack_images.value:
            return stack_images_node.get_metadata()
        case _:
            return metadata
