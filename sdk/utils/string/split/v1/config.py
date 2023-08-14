from pydantic import Field
from hyko_sdk import extract_metadata, CoreModel

description = "Split a string to a list of strings based on delimiter"

class Inputs(CoreModel):
    text: str = Field(..., description="Input text")

class Params(CoreModel):
    delimeter: str = Field(default=',', description="the string used to split the text by")

class Outputs(CoreModel):
    splitted: list[str]  = Field(..., description="List of strings that resulted from splitting by the delimeter")

if __name__ == "__main__":
    extract_metadata(
                    Inputs, Params, Outputs,  # type: ignore
                    description, False
                )