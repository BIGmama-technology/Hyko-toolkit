from pydantic import Field

from hyko_sdk.function import SDKFunction
from hyko_sdk.metadata import CoreModel

func = SDKFunction(description="Recursive Character Text Splitter Tool.")


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
    result: str = Field(..., description="Processed text with chunks")
