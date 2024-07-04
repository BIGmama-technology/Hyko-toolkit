from typing import Any

from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.exceptions import APICallError

node = ToolkitNode(
    name="Retrieve an element",
    cost=0,
    description="Gets an element from a slit based on the index",
)


@node.set_input
class Inputs(CoreModel):
    original_list: list[str] = field(description="The original list.")


@node.set_param
class Params(CoreModel):
    index: int = field(description="The index of the element to retrieve")


@node.set_output
class Outputs(CoreModel):
    output: Any = field(
        description="The retrieved element",
    )


@node.on_call
async def call(inputs: Inputs, params: Params) -> Outputs:
    if int(params.index) > len(inputs.original_list) - 1:
        raise APICallError

    element = inputs.original_list[int(params.index)]
    return Outputs(output=element)
