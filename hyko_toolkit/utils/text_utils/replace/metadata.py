from enum import Enum

from fastapi import HTTPException
from hyko_sdk.models import CoreModel
from pydantic import Field

from hyko_toolkit.registry import ToolkitUtils

func = ToolkitUtils(
    name="replace",
    task="text_utils",
    description="Replace occurrences of a substring in a string",
)


class ReplaceMode(str, Enum):
    replace_all = "replaceAll"
    replace_first = "replaceFirst"


@func.set_input
class Inputs(CoreModel):
    text: str = Field(..., description="Input text")


@func.set_param
class Params(CoreModel):
    old_substring: str = Field(..., description="Substring to replace")
    new_substring: str = Field(..., description="Replacement string")
    replace_mode: ReplaceMode = Field(
        default=ReplaceMode.replace_all,
        description="Replace mode: replaceAll or replaceFirst",
    )


@func.set_output
class Outputs(CoreModel):
    replaced: str = Field(..., description="Text with replaced occurrences")


@func.on_call
async def call(inputs: Inputs, params: Params) -> Outputs:
    if params.replace_mode == ReplaceMode.replace_all:
        replaced_text = inputs.text.replace(params.old_substring, params.new_substring)
    elif params.replace_mode == ReplaceMode.replace_first:
        replaced_text = inputs.text.replace(
            params.old_substring, params.new_substring, 1
        )
    else:
        raise HTTPException(
            status_code=500, detail=f"Invalid relace mode'{params.replace_mode}'."
        )

    return Outputs(replaced=replaced_text)
