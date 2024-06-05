from hyko_sdk.components.components import TextField, TextPreview
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

input_node = ToolkitNode(
    name="Text",
    description="Write your text.",
    icon="text",
    cost=0,
)


@input_node.set_output
class Output(CoreModel):
    output_text: str = field(
        description="input text",
        component=TextField(placeholder="input text here.", multiline=True),
    )


output_node = ToolkitNode(
    name="Text",
    description="Preview output text.",
    icon="text",
    cost=0,
)


@output_node.set_input
class Input(CoreModel):
    input_text: str = field(
        description="output text",
        component=TextPreview(),
    )
