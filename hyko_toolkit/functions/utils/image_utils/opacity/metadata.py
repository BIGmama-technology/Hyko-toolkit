from hyko_sdk.io import Image
from hyko_sdk.models import CoreModel
from pydantic import Field, PositiveFloat

from hyko_toolkit.registry import ToolkitFunction

func = ToolkitFunction(
    name="opacity",
    task="image_utils",
    description="Adjusts the opacity of an image",
    absolute_dockerfile_path="./toolkit/hyko_toolkit/functions/utils/image_utils/Dockerfile",
    docker_context="./toolkit/hyko_toolkit/functions/utils/image_utils/opacity",
)


@func.set_input
class Inputs(CoreModel):
    image: Image = Field(..., description="Input image to adjust opacity")


@func.set_param
class Params(CoreModel):
    opacity: PositiveFloat = Field(
        default=50, le=100, description="Opacity value (0-100)"
    )


@func.set_output
class Outputs(CoreModel):
    adjusted_image: Image = Field(..., description="Image with adjusted opacity")
