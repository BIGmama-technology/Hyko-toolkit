from hyko_sdk.components.components import TextField, TextPreview
from hyko_sdk.models import Category, CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.registry import ToolkitNode

input_node = ToolkitNode(
    name="Text",
    task="inputs",
    description="Write your text.",
    category=Category.IO,
    cost=0,
)


@input_node.set_output
class Output(CoreModel):
    output_text: str = field(
        description="inpt text",
        component=TextField(placeholder="input text here.", multiline=True),
    )


output_node = ToolkitNode(
    name="Text",
    task="outputs",
    description="Preview output text.",
    category=Category.IO,
    cost=0,
)


@output_node.set_input
class Input(CoreModel):
    input_text: str = field(
        description="output text",
        component=TextPreview(),
    )
