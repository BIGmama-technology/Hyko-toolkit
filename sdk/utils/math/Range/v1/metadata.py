from pydantic import Field

from hyko_sdk.function import SDKFunction
from hyko_sdk.metadata import CoreModel

func = SDKFunction(
    description="Generate a range of integers",
)


@func.set_input
class Inputs(CoreModel):
    pass


@func.set_param
class Params(CoreModel):
    start: int = Field(..., description="Start integer in the range")
    end: int = Field(..., description="End integer (not included in the range)")


@func.set_output
class Outputs(CoreModel):
    result: list[int] = Field(..., description="Output range")
