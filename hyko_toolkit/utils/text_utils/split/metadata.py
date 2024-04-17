from hyko_sdk.models import CoreModel
from pydantic import Field

from hyko_toolkit.utils.utils_registry import ToolkitUtils

func = ToolkitUtils(
    name="split",
    task="text_utils",
    description="Split a string to a list of strings based on delimiter",
)


@func.set_input
class Inputs(CoreModel):
    text: str = Field(..., description="Input text")


@func.set_param
class Params(CoreModel):
    delimiter: str = Field(
        default=",", description="the string used to split the text by"
    )


@func.set_output
class Outputs(CoreModel):
    splitted: list[str] = Field(
        ..., description="List of strings that resulted from splitting by the delimeter"
    )


@func.on_call
async def call(inputs: Inputs, params: Params) -> Outputs:
    return Outputs(splitted=inputs.text.split(params.delimiter))
