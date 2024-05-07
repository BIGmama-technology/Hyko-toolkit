from hyko_sdk.components import NumberField
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.registry import ToolkitIO

input_node = ToolkitIO(
    name="number",
    task="inputs",
    description="Input number.",
)


@input_node.set_output
class Output(CoreModel):
    output_number: float = field(
        description=" Input number", component=NumberField(placeholder="help")
    )


output_node = ToolkitIO(
    name="number",
    task="outputs",
    description="Output number.",
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
