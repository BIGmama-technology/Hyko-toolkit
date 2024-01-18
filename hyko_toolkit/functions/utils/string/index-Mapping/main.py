from typing import List

from fastapi import HTTPException
from metadata import Inputs, Outputs, Params, func


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    input_strings = inputs.input_strings
    indexes = inputs.indexes

    output_strings: List[str] = []

    for i in indexes:
        if 0 <= i < len(input_strings):
            output_strings.append(input_strings[i])
        else:
            raise HTTPException(
                status_code=500,
                detail=f"Index {i} is out of bounds for the input list of strings.",
            )
    return Outputs(output_strings=output_strings)
