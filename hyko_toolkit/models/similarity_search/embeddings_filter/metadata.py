from pydantic import Field

from hyko_sdk.definitions import ToolkitModel
from hyko_sdk.models import CoreModel

func = ToolkitModel(
    name="embeddings_filter",
    task="similarity_search",
    description="Document compressor that uses embeddings to drop documents unrelated to the query.",
)


@func.set_input
class Inputs(CoreModel):
    docs: list[str] = Field(
        ...,
        description="Text Input.",
    )
    query: str = Field(
        ...,
        description="Query or the Question to compare against the input text.",
    )


@func.set_param
class Params(CoreModel):
    embeddings_similarity_threshold: float = Field(
        default=0.6,
        description="Threshold for determining when two documents are similar enough to be considered redundant (default=0.6).",
    )
    top_k: int = Field(
        default=5,
        description="Number of top results to consider (default=5).",
    )
    score_threshold: float = Field(
        default=0.5,
        description="Threshold score to filter similarity results (default=0.5).",
    )


@func.set_output
class Outputs(CoreModel):
    result: list[str] = Field(..., description="Top K results.")
