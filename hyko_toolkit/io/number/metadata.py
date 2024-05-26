from hyko_sdk.components.components import NumberField
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.registry import ToolkitIO

input_node = ToolkitIO(
    name="Number", task="Inputs", description="Input number.", icon="number"
)


@input_node.set_output
class Output(CoreModel):
    output_number: float = field(
        description=" Input number",
        component=NumberField(placeholder="your input number"),
    )


output_node = ToolkitIO(
    name="Number", task="Outputs", description="Output number.", icon="number"
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
