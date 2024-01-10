from pydantic import Field

from hyko_sdk.function import SDKFunction
from hyko_sdk.metadata import CoreModel

func = SDKFunction(
    description="Count the number of occurrences of a substring in a string",
    requires_gpu=False,
)


@func.set_input
class Inputs(CoreModel):
    text: str = Field(..., description="Input text")


@func.set_param
class Params(CoreModel):
    substring: str = Field(..., description="The substring to count")


@func.set_output
class Outputs(CoreModel):
    count: int = Field(..., description="Number of occurrences of the substring")
