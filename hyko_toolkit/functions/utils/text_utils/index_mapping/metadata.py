from hyko_sdk.definitions import ToolkitFunction
from hyko_sdk.models import CoreModel
from pydantic import Field

func = ToolkitFunction(
    name="index_mapping",
    task="text_utils",
    description="Map indexes to strings and return the corresponding strings",
)


@func.set_input
class Inputs(CoreModel):
    input_strings: list[str] = Field(..., description="list of input strings")
    indexes: list[int] = Field(..., description="list of indexes")


@func.set_output
class Outputs(CoreModel):
    output_strings: list[str] = Field(..., description="list of mapped output strings")
