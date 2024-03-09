from pydantic import Field

from hyko_sdk.definitions import SDKFunction
from hyko_sdk.metadata import CoreModel

func = SDKFunction(description="Search the web using DuckDuckGo.")


@func.set_input
class Inputs(CoreModel):
    query: str = Field(
        ...,
        description="The search query.",
    )


@func.set_param
class Params(CoreModel):
    max_results: int = Field(
        ...,
        description="Maximum number of search.",
    )


@func.set_output
class Outputs(CoreModel):
    result: str = Field(..., description="The concatenated titles and summaries.")
