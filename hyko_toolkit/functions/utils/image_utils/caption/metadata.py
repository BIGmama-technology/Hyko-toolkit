from enum import Enum

from hyko_sdk.io import Image
from hyko_sdk.models import CoreModel
from pydantic import Field, PositiveInt

from hyko_toolkit.registry import ToolkitFunction

func = ToolkitFunction(
    name="caption",
    task="image_utils",
    description="Add caption to an image",
    absolute_dockerfile_path="./toolkit/hyko_toolkit/functions/utils/image_utils/Dockerfile",
    docker_context="./toolkit/hyko_toolkit/functions/utils/image_utils/caption",
)


class CaptionColor(str, Enum):
    WHITE = "white"
    BLACK = "black"


class CaptionPosition(str, Enum):
    TOP = "top"
    BOTTOM = "bottom"


@func.set_input
class Inputs(CoreModel):
    input_image: Image = Field(..., description="Input image to add a caption to")
    caption: str = Field(..., description="Caption text to be added")


@func.set_param
class Params(CoreModel):
    caption_size: PositiveInt = Field(default=12, description="Caption size in pixels")
    caption_color: CaptionColor = Field(
        default=CaptionColor.BLACK, description="Caption color: white or black"
    )
    position: CaptionPosition = Field(
        default=CaptionPosition.TOP, description="Position to add the caption"
    )


@func.set_output
class Outputs(CoreModel):
    captioned_image: Image = Field(..., description="Image with added caption")
