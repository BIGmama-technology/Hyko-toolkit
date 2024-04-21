from hyko_sdk.models import CoreModel
from pydantic import Field

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
    text: str = Field(..., description="Text Input")


@func.set_param
class Params(CoreModel):
    chunk_size: int = Field(..., description="Chunk size")
    chunk_overlap: int = Field(..., description="Chunk overlap")


@func.set_output
class Outputs(CoreModel):
    chunks: list[str] = Field(..., description="Processed text with chunks")
