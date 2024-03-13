from pydantic import Field

from hyko_sdk.definitions import ToolkitFunction
from hyko_sdk.models import CoreModel

func = ToolkitFunction(
    name="random",
    task="math_utils",
    description="Generate a random integer",
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
