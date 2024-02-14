from pydantic import Field

from hyko_sdk.function import SDKFunction
from hyko_sdk.metadata import CoreModel

func = SDKFunction(
    description="Tool for computing similarity scores based on a given threshold."
)


@func.set_input
class Inputs(CoreModel):
    text: str = Field(
        ...,
        description="Text Input. ",
    )


@func.set_startup_params
class StartupParams(CoreModel):
    pass


@func.set_param
class Params(CoreModel):
    query: str = Field(
        ...,
        description="Query to compare against the input text.",
    )
    top_k: int = Field(
        ...,
        description="Number of top results to consider. ",
    )
    score_threshold: float = Field(
        ...,
        description="Threshold score to filter similarity results. ",
    )


@func.set_output
class Outputs(CoreModel):
    result: str = Field(..., description="Top K results. ")
