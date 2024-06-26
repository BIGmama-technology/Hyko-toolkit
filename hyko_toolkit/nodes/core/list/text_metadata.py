from hyko_sdk.components.components import ListComponent, TextField
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

input_node = ToolkitNode(
    name="List of text input",
    description="input list of text.",
    icon="list",
    cost=0,
)


@input_node.set_output
class Output(CoreModel):
    output_list: list[str] = field(
        description="input list of text.",
        component=ListComponent(
            item_component=TextField(placeholder="text item", multiline=False)
        ),
    )


output_node = ToolkitNode(
    name="List of text output",
    description="output list of text.",
    icon="list",
    is_output=True,
)


@output_node.set_input
class Input(CoreModel):
    output_list: list[str] = field(
        description="output list of text",
        component=ListComponent(
            freezed=True,
            item_component=TextField(
                placeholder="text item",
                multiline=False,
                freezed=True,
            ),
        ),
    )
