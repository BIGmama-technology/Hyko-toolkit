from hyko_sdk.components.components import TextField, TextPreview
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.registry import ToolkitIO

input_node = ToolkitIO(
    name="Text", task="Inputs", description="Write your text.", icon="text"
)


@input_node.set_output
class Output(CoreModel):
    output_text: str = field(
        description="input text",
        component=TextField(placeholder="input text here.", multiline=True),
    )


output_node = ToolkitIO(
    name="Text", task="Outputs", description="Preview output text.", icon="text"
)


@output_node.set_input
class Input(CoreModel):
    input_text: str = field(
        description="output text",
        component=TextPreview(),
    )
