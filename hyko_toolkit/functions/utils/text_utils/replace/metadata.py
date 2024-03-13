from enum import Enum

from pydantic import Field

from hyko_sdk.definitions import ToolkitFunction
from hyko_sdk.models import CoreModel

func = ToolkitFunction(
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
        ..., description="Replace mode: replaceAll or replaceFirst"
    )


@func.set_output
class Outputs(CoreModel):
    replaced: str = Field(..., description="Text with replaced occurrences")
