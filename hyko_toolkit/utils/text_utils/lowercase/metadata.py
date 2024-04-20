from hyko_sdk.models import CoreModel
from pydantic import Field

from hyko_toolkit.utils.utils_registry import ToolkitUtils

func = ToolkitUtils(
    name="lowercase",
    task="text_utils",
    description="Convert a given string to lowercase",
)


@func.set_input
class Inputs(CoreModel):
    text: str = Field(..., description="Input text")


@func.set_param
class Params(CoreModel):
    pass


@func.set_output
class Outputs(CoreModel):
    lowercase_string: str = Field(
        ..., description="Lowercase version of the input string"
    )


@func.on_call
async def call(inputs: Inputs, params: Params) -> Outputs:
    lowercase_string = inputs.text.lower()
    return Outputs(lowercase_string=lowercase_string)
