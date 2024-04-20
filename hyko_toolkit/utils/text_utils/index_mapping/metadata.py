from fastapi import HTTPException
from hyko_sdk.models import CoreModel
from pydantic import Field

from hyko_toolkit.utils.utils_registry import ToolkitUtils

func = ToolkitUtils(
    name="index_mapping",
    task="text_utils",
    description="Map indexes to strings and return the corresponding strings",
)


@func.set_input
class Inputs(CoreModel):
    input_strings: list[str] = Field(..., description="list of input strings")
    indexes: list[int] = Field(..., description="list of indexes")


@func.set_param
class Params(CoreModel):
    pass


@func.set_output
class Outputs(CoreModel):
    output_strings: list[str] = Field(..., description="list of mapped output strings")


@func.on_call
async def call(inputs: Inputs, params: Params) -> Outputs:
    input_strings = inputs.input_strings
    indexes = inputs.indexes

    output_strings: list[str] = []

    for i in indexes:
        if 0 <= i < len(input_strings):
            output_strings.append(input_strings[i])
        else:
            raise HTTPException(
                status_code=500,
                detail=f"Index {i} is out of bounds for the input list of strings.",
            )
    return Outputs(output_strings=output_strings)
