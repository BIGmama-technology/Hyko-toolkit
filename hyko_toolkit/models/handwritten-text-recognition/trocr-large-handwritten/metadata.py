from pydantic import Field

from hyko_sdk.function import SDKFunction
from hyko_sdk.io import Image
from hyko_sdk.metadata import CoreModel

func = SDKFunction(
    description="Perform Handwritten Text Recognition on an input image",
)


@func.set_startup_params
class StartupParams(CoreModel):
    device_map: str = Field(..., description="Device map (Auto, CPU or GPU)")


@func.set_input
class Inputs(CoreModel):
    image: Image = Field(..., description="Input image containing handwritten text")


@func.set_param
class Params(CoreModel):
    pass


@func.set_output
class Outputs(CoreModel):
    generated_text: str = Field(..., description="Recognized text from the input image")
