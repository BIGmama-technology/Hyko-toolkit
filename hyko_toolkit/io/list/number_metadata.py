from hyko_sdk.components.components import ListComponent, NumberField
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.registry import ToolkitIO

input_node = ToolkitIO(
    name="list of numbers",
    task="inputs",
    description="input list of numbers.",
)


@input_node.set_output
class Output(CoreModel):
    output_list: list[float] = field(
        description="input list of numbers.",
        component=ListComponent(item_component=NumberField(placeholder="number item")),
    )


output_node = ToolkitIO(
    name="list of number",
    task="outputs",
    description="output list of numbers.",
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
