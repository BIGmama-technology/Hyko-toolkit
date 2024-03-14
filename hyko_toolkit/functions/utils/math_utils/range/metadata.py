from hyko_sdk.definitions import ToolkitFunction
from hyko_sdk.models import CoreModel
from pydantic import Field

func = ToolkitFunction(
    name="range",
    task="math_utils",
    description="Generate a range of integers",
)


@func.set_param
class Params(CoreModel):
    start: int = Field(..., description="Start integer in the range")
    end: int = Field(..., description="End integer (not included in the range)")


@func.set_output
class Outputs(CoreModel):
    result: list[int] = Field(..., description="Output range")
