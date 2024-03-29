from hyko_sdk.definitions import ToolkitFunction
from hyko_sdk.models import CoreModel
from pydantic import Field

func = ToolkitFunction(
    name="remove_special_characters",
    task="nlp_utils",
    description="A function to remove special characters and punctuation from text.",
)


@func.set_input
class Inputs(CoreModel):
    text: str = Field(
        ...,
        description="The input text from which special characters and punctuation will be removed.",
    )


@func.set_output
class Outputs(CoreModel):
    result: str = Field(
        ..., description="The text with special characters and punctuation removed."
    )
