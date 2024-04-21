from hyko_sdk.io import Image
from hyko_sdk.models import CoreModel
from pydantic import Field

from hyko_toolkit.registry import ToolkitFunction

func = ToolkitFunction(
    name="rotate",
    task="image_utils",
    description="Rotate an image by a given angle",
    absolute_dockerfile_path="./toolkit/hyko_toolkit/functions/utils/image_utils/Dockerfile",
    docker_context="./toolkit/hyko_toolkit/functions/utils/image_utils/rotate",
)


@func.set_input
class Inputs(CoreModel):
    image: Image = Field(..., description="Input image to be rotated")


@func.set_param
class Params(CoreModel):
    rotation_angle: int = Field(default=30, description="Rotation angle in degrees")


@func.set_output
class Outputs(CoreModel):
    rotated_image: Image = Field(..., description="Rotated image")
