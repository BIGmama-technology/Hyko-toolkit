from pydantic import Field

from hyko_sdk.function import SDKFunction
from hyko_sdk.metadata import CoreModel

func = SDKFunction(
    description="Executes simultaneous BM25 keyword matching and document similarity searches on input documents."
)


@func.set_startup_params
class StartupParams(CoreModel):
    pass


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
    bm25_k: int = Field(
        ...,
        description="Number of top results to consider in Best Matching Algorithm (BM25).",
    )
    faiss_k: int = Field(
        ...,
        description="Number of top results to consider in Similarity Search Algorithm.",
    )


@func.set_output
class Outputs(CoreModel):
    result: list[str] = Field(..., description="Top K results.")
