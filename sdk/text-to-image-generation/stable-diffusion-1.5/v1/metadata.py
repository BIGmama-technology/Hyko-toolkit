from pydantic import Field

from hyko_sdk.function import SDKFunction
from hyko_sdk.io import Image
from hyko_sdk.metadata import CoreModel

func = SDKFunction(
    description="Text to Image Generation Model",
)


@func.set_input
class Inputs(CoreModel):
    prompt: str = Field(..., description="User text prompt")


@func.set_param
class Params(CoreModel):
    device_map: str = Field(..., description="Device map (Auto, CPU or GPU)")


@func.set_output
class Outputs(CoreModel):
    generated_image: Image = Field(
        ..., description="AI Generated image described by user text prompt"
    )
