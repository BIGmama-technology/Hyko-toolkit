from pydantic import Field

from hyko_sdk.definitions import ToolkitModel
from hyko_sdk.models import CoreModel

func = ToolkitModel(
    name="bm25",
    task="similarity_search",
    description="Perform BM25 retrieval on a list of documents based on a given query.",
)


@func.set_input
class Inputs(CoreModel):
    docs: list[str] = Field(
        ...,
        description="Input Documents.",
    )
    query: str = Field(
        ...,
        description="Query or the Question to compare against the input text.",
    )


@func.set_param
class Params(CoreModel):
    top_k: int = Field(
        default=3,
        description="Number of top results to consider (default=3).",
    )


@func.set_output
class Outputs(CoreModel):
    result: list[str] = Field(..., description="Top K results.")
