from pydantic import Field

from hyko_sdk.function import SDKFunction
from hyko_sdk.metadata import CoreModel

func = SDKFunction(
    description="Generate a random integer",
    requires_gpu=False,
)


@func.set_input
class Inputs(CoreModel):
    pass


@func.set_param
class Params(CoreModel):
    min_val: int = Field(..., description="Minimum value for random number generation")
    max_val: int = Field(..., description="Maximum value for random number generation")


@func.set_output
class Outputs(CoreModel):
    result: int = Field(..., description="Generated random number")
