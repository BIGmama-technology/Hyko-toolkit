from hyko_sdk.components.components import TextField
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

node = ToolkitNode(
    name="recursive_character_text_splitter",
    cost=3,
    description="Divides text recursively based on specified characters, ensuring semantic coherence.",
    require_worker=True,
)


@node.set_input
class Inputs(CoreModel):
    text: str = field(
        description="Text Input",
        component=TextField(placeholder="Entre your text here", multiline=True),
    )


@node.set_param
class Params(CoreModel):
    chunk_size: int = field(description="Chunk size")
    chunk_overlap: int = field(
        description="Chunk overlap",
    )


@node.set_output
class Outputs(CoreModel):
    chunks: list[str] = field(description="Processed text with chunks")
