from pydantic import Field

from hyko_sdk.function import SDKFunction
from hyko_sdk.metadata import CoreModel

func = SDKFunction(
    description="A tool employing Flashrank re-ranking capabilities for enhancing search and retrieval pipelines, leveraging state-of-the-art cross-encoders."
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
    result: list[str] = Field(..., description="Top K results. ")
