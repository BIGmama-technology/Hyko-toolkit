from enum import Enum

from fastapi import HTTPException
from pydantic import Field

from hyko_sdk.function import SDKFunction
from hyko_sdk.metadata import CoreModel

func = SDKFunction(
    description="Replace occurrences of a substring in a string",
    requires_gpu=False,
)


class ReplaceMode(str, Enum):
    replaceAll = "replaceAll"
    replaceFirst = "replaceFirst"


class Inputs(CoreModel):
    text: str = Field(..., description="Input text")


class Params(CoreModel):
    old_substring: str = Field(..., description="Substring to replace")
    new_substring: str = Field(..., description="Replacement string")
    replace_mode: ReplaceMode = Field(
        ..., description="Replace mode: replaceAll or replaceFirst"
    )


class Outputs(CoreModel):
    replaced: str = Field(..., description="Text with replaced occurrences")


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    if params.replace_mode == ReplaceMode.replaceAll:
        replaced_text = inputs.text.replace(params.old_substring, params.new_substring)
    elif params.replace_mode == ReplaceMode.replaceFirst:
        replaced_text = inputs.text.replace(
            params.old_substring, params.new_substring, 1
        )
    else:
        raise HTTPException(
            status_code=500, detail=f"Invalid relace mode'{params.replace_mode}'."
        )

    return Outputs(replaced=replaced_text)
