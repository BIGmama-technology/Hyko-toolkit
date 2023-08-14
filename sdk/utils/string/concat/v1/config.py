from pydantic import Field
from hyko_sdk import CoreModel, extract_metadata

description = "Concatenate two strings together"

class Inputs(CoreModel):
    pass

class Params(CoreModel):
    first: str = Field(..., description="First string")
    second: str = Field(..., description="Second string")

class Outputs(CoreModel):
    output: str = Field(..., description="Concatenated result")

if __name__ == "__main__":
    extract_metadata(
                    Inputs, Params, Outputs,  # type: ignore
                    description, False
                )