from pydantic import Field

from hyko_sdk.function import SDKFunction
from hyko_sdk.metadata import CoreModel

func = SDKFunction(
    description="Takes a list of strings and a query and returns the top K most similar sentences to the query",
)


@func.set_input
class Inputs(CoreModel):
    sentences: list[str] = Field(..., description="List of sentences to search in")


@func.set_param
class Params(CoreModel):
    query: str = Field(..., description="Query string")
    top_k: int = Field(default=5, description="Number of sentences to output")


@func.set_output
class Outputs(CoreModel):
    selected_sentences: list[str] = Field(
        ..., description="List of top k elected sentences"
    )
