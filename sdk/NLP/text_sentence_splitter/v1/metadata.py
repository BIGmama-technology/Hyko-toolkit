from pydantic import Field

from hyko_sdk.function import SDKFunction
from hyko_sdk.metadata import CoreModel

func = SDKFunction(
    description="Takes a paragraph and tokenizes (splits) it into a list of sentences",
)


@func.set_input
class Inputs(CoreModel):
    text: str = Field(..., description="Text to be split")


@func.set_param
class Params(CoreModel):
    pass


@func.set_output
class Outputs(CoreModel):
    sentences: list[str] = Field(..., description="Splitted sentences")
