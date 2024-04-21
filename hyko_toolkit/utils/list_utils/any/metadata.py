from typing import Any

from hyko_sdk.models import CoreModel
from pydantic import Field

from hyko_toolkit.utils.utils_registry import ToolkitUtils

func = ToolkitUtils(
    name="any_value",
    task="list_utils",
    description="Returns True if any element of the list is equal a certain value.",
)


@func.set_input
class Inputs(CoreModel):
    original_list: list[Any] = Field(
        ...,
        description="The original list.",
    )
    value: Any = Field(
        ...,
        description="The value to be checked.",
    )


@func.set_param
class Params(CoreModel):
    pass


@func.set_output
class Outputs(CoreModel):
    output: bool = Field(
        ...,
        description="Final list.",
    )


@func.on_call
async def call(inputs: Inputs, params: Params) -> Outputs:
    lst = inputs.original_list
    return Outputs(output=any(element == inputs.value for element in lst))
