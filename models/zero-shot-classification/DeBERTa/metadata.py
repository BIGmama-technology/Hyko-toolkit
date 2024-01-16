from pydantic import Field

from hyko_sdk.function import SDKFunction
from hyko_sdk.metadata import CoreModel

func = SDKFunction(
    description="Perform zero-shot classification on text input, assigning it to one of the predefined classes",
)


@func.set_input
class Inputs(CoreModel):
    text: str = Field(..., description="Input text to be classified")
    classes: list[str] = Field(..., description="A list of possible classes")


@func.set_param
class Params(CoreModel):
    pass


@func.set_output
class Outputs(CoreModel):
    output_class: str = Field(..., description="The predicted class")
