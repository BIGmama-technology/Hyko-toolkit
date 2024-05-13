from hyko_sdk.components.components import TextField
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.registry import ToolkitFunction

func = ToolkitFunction(
    name="recursive_character_text_splitter",
    task="nlp_utils",
    description="Divides text recursively based on specified characters, ensuring semantic coherence.",
    absolute_dockerfile_path="./toolkit/hyko_toolkit/functions/utils/nlp_utils/recursive_character_text_splitter/Dockerfile",
    docker_context="./toolkit/hyko_toolkit/functions/utils/nlp_utils/recursive_character_text_splitter",
)


@func.set_input
class Inputs(CoreModel):
    text: str = field(
        description="Text Input",
        component=TextField(placeholder="Entre your text here", multiline=True),
    )


@func.set_param
class Params(CoreModel):
    chunk_size: int = field(description="Chunk size")
    chunk_overlap: int = field(
        description="Chunk overlap",
    )


@func.set_output
class Outputs(CoreModel):
    chunks: list[str] = field(description="Processed text with chunks")
