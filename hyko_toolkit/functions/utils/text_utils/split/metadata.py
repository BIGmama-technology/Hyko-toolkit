from pydantic import Field

from hyko_sdk.definitions import ToolkitFunction
from hyko_sdk.models import CoreModel

func = ToolkitFunction(
    description="Split a string to a list of strings based on delimiter",
)


@func.set_input
class Inputs(CoreModel):
    text: str = Field(..., description="Input text")


@func.set_param
class Params(CoreModel):
    delimeter: str = Field(
        default=",", description="the string used to split the text by"
    )


@func.set_output
class Outputs(CoreModel):
    splitted: list[str] = Field(
        ..., description="List of strings that resulted from splitting by the delimeter"
    )
