from hyko_sdk.definitions import ToolkitFunction
from hyko_sdk.models import CoreModel
from pydantic import Field

func = ToolkitFunction(
    name="recursive_character_text_splitter",
    task="nlp_utils",
    description="Divides text recursively based on specified characters, ensuring semantic coherence.",
)


@func.set_input
class Inputs(CoreModel):
    text: str = Field(
        ...,
        description="Text Input",
    )


@func.set_param
class Params(CoreModel):
    chunk_size: int = Field(
        ...,
        description="Chunk size",
    )
    chunk_overlap: int = Field(
        ...,
        description="Chunk overlap",
    )


@func.set_output
class Outputs(CoreModel):
    chunks: list[str] = Field(..., description="Processed text with chunks")
