from fastapi import HTTPException
from hyko_sdk.components.components import ListComponent, NumberField, TextField
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

node = ToolkitNode(
    name="Index mapping",
    cost=0,
    description="Map indexes to strings and return the corresponding strings",
)


@node.set_input
class Inputs(CoreModel):
    input_strings: list[str] = field(
        description="list of input strings",
        component=ListComponent(
            item_component=TextField(placeholder="Enter your text here", multiline=True)
        ),
    )
    indexes: list[int] = field(
        description="list of indexes",
        component=ListComponent(
            item_component=NumberField(placeholder="Enter your text here")
        ),
    )


@node.set_param
class Params(CoreModel):
    pass


@node.set_output
class Outputs(CoreModel):
    output_strings: list[str] = field(description="list of mapped output strings")


@node.on_call
async def call(inputs: Inputs, params: Params) -> Outputs:
    input_strings = inputs.input_strings
    indexes = inputs.indexes

    output_strings: list[str] = []

    for i in indexes:
        if 0 <= i < len(input_strings):
            output_strings.append(input_strings[i])
        else:
            raise HTTPException(
                status_code=500,
                detail=f"Index {i} is out of bounds for the input list of strings.",
            )
    return Outputs(output_strings=output_strings)
