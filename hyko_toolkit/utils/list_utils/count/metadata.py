from typing import Any

from hyko_sdk.models import Category, CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.registry import Toolkit

func = Toolkit(
    category=Category.UTILS,
    name="count_element",
    task="list_utils",
    cost=0,
    description="Counts the number of occurrences of an element in a list.",
)


@func.set_input
class Inputs(CoreModel):
    original_list: list[Any] = field(
        description="The original list.",
    )
    element: Any = field(
        description="The element to be counted in the list.",
    )


@func.set_param
class Params(CoreModel):
    pass


@func.set_output
class Outputs(CoreModel):
    output: int = field(
        description="Final list.",
    )


def count_element(lst: list[Any], element: Any) -> int:
    return lst.count(element)


@func.on_call
async def call(inputs: Inputs, params: Params) -> Outputs:
    lst = inputs.original_list
    return Outputs(output=lst.count(inputs.element))
