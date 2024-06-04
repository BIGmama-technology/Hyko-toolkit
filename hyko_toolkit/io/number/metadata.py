from hyko_sdk.components.components import NumberField
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.models import Category, CoreModel
from hyko_sdk.utils import field

input_node = ToolkitNode(
    name="number",
    task="inputs",
    description="Input number.",
    icon="number",
    category=Category.IO,
    cost=0,
)


@input_node.set_output
class Output(CoreModel):
    output_number: float = field(
        description=" Input number",
        component=NumberField(placeholder="your input number"),
    )


output_node = ToolkitNode(
    name="number",
    task="outputs",
    icon="number",
    description="Output number.",
    category=Category.IO,
    cost=0,
)


@output_node.set_input
class Input(CoreModel):
    output_number: float = field(
        description="Output number",
        component=NumberField(
            placeholder="output number",
            freezed=True,
        ),
    )
