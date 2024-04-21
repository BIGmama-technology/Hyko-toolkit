from typing import Any, Iterable

from hyko_sdk.models import CoreModel
from pydantic import Field

from hyko_toolkit.utils.utils_registry import ToolkitUtils

func = ToolkitUtils(
    name="extend_list",
    task="list_utils",
    description="Extends a list with another list.",
)


@func.set_input
class Inputs(CoreModel):
    original_list: list[Any] = Field(
        ...,
        description="The list to be extended.",
    )
    iterable: Any = Field(
        ...,
        description="List of elements to be appended to the original list.",
    )


@func.set_param
class Params(CoreModel):
    pass


@func.set_output
class Outputs(CoreModel):
    output: Any = Field(
        ...,
        description="Final list.",
    )


def extend_list(lst: list[Any], iterable: Iterable[Any]) -> list[Any]:
    lst.extend(iterable)
    return lst


@func.on_call
async def call(inputs: Inputs, params: Params) -> Outputs:
    lst = inputs.original_list
    lst.extend(inputs.iterable)
    return Outputs(output=lst)
