from hyko_sdk.components.components import NumberField
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

input_node = ToolkitNode(
    name="Number input",
    description="Input number.",
    icon="number",
    is_input=True,
)


@input_node.set_output
class Output(CoreModel):
    output_number: float = field(
        description=" Input number",
        component=NumberField(placeholder="your input number"),
    )


output_node = ToolkitNode(
    name="Number output",
    icon="number",
    description="Output number.",
    is_output=True,
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
