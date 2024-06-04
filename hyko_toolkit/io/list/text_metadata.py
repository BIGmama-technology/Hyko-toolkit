from hyko_sdk.components.components import ListComponent, TextField
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.models import Category, CoreModel
from hyko_sdk.utils import field

input_node = ToolkitNode(
    name="list of text",
    task="inputs",
    description="input list of text.",
    category=Category.IO,
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
    name="list of text",
    task="outputs",
    description="output list of text.",
    category=Category.IO,
    icon="list",
    cost=0,
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
