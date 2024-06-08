from hyko_sdk.components.components import ListComponent, NumberField
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

input_node = ToolkitNode(
    name="List of numbers input",
    description="input list of numbers.",
    icon="list",
    is_input=True,
)


@input_node.set_output
class Output(CoreModel):
    output_list: list[float] = field(
        description="input list of numbers.",
        component=ListComponent(item_component=NumberField(placeholder="number item")),
    )


output_node = ToolkitNode(
    name="List of number output",
    icon="list",
    description="output list of numbers.",
    is_output=True,
)


@output_node.set_input
class Input(CoreModel):
    output_list: list[float] = field(
        description="output list of numbers",
        component=ListComponent(
            freezed=True,
            item_component=NumberField(
                placeholder="number item",
                freezed=True,
            ),
        ),
    )
