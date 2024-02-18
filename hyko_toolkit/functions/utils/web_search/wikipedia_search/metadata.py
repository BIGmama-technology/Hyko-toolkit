from enum import Enum

from pydantic import Field

from hyko_sdk.function import SDKFunction
from hyko_sdk.metadata import CoreModel


class SupportedLanguages(str, Enum):
    english = "en"
    arabic = "ar"
    french = "fr"


func = SDKFunction(description="Search wikipedia summaries.")


@func.set_input
class Inputs(CoreModel):
    query: str = Field(
        ...,
        description="The search query.",
    )


@func.set_param
class Params(CoreModel):
    num_results: int = Field(
        ...,
        description="Number of search results to return.",
    )
    language: SupportedLanguages = Field(
        ...,
        description="The search Language.",
    )


@func.set_output
class Outputs(CoreModel):
    result: str = Field(..., description="The concatenated titles and summaries.")
