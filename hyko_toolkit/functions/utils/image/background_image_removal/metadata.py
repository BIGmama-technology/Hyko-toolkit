from pydantic import Field

from hyko_sdk.function import SDKFunction
from hyko_sdk.io import Image
from hyko_sdk.metadata import CoreModel

func = SDKFunction(
    description="",
)


@func.set_input
class Inputs(CoreModel):
    input_image: Image = Field(..., description="Original image")


@func.set_param
class Params(CoreModel):
    pass


@func.set_output
class Outputs(CoreModel):
    image: Image = Field(..., description="Image without background")
