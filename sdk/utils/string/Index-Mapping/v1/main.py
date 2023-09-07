from fastapi import HTTPException
from pydantic import Field
from hyko_sdk import CoreModel, SDKFunction
from typing import List


func = SDKFunction(
    description="Map indexes to strings and return the corresponding strings",
    requires_gpu=False,
)

class Inputs(CoreModel):
    input_strings: List[str] = Field(..., description="List of input strings")


class Params(CoreModel):
    indexes: List[int] = Field(..., description="List of indexes")


class Outputs(CoreModel):
    output_strings: List[str] = Field(..., description="List of mapped output strings")


@func.on_execute
async def main(inputs: Inputs , params: Params)-> Outputs:
    input_strings = inputs.input_strings
    indexes = params.indexes

    output_strings: List[str] = []

    for i in indexes:
        if 0 <= i < len(input_strings):
            output_strings.append(input_strings[i])
        else:
           raise HTTPException(
                status_code=500,
                detail=f"Index {i} is out of bounds for the input list of strings."
            )
    return Outputs(output_strings=output_strings)

