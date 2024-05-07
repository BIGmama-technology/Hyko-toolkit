from hyko_sdk.components import ListComponent, TextField
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.registry import ToolkitIO

input_node = ToolkitIO(
    name="list of text",
    task="inputs",
    description="input list of text.",
)


@input_node.set_output
class Output(CoreModel):
    output_list: list[str] = field(
        description="input list of text.",
        component=ListComponent(
            item_component=TextField(placeholder="text item", multiline=False)
        ),
    )


output_node = ToolkitIO(
    name="list of text",
    task="outputs",
    description="output list of text.",
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
