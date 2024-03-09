from pydantic import Field

from hyko_sdk.definitions import SDKFunction
from hyko_sdk.metadata import CoreModel

func = SDKFunction(
    description="Concatenate two strings together",
)


@func.set_input
class Inputs(CoreModel):
    first: str = Field(..., description="First string")
    second: str = Field(..., description="Second string")


@func.set_param
class Params(CoreModel):
    pass


@func.set_output
class Outputs(CoreModel):
    output: str = Field(..., description="Concatenated result")
