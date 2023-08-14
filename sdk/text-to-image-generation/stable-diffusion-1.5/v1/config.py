from pydantic import Field
from hyko_sdk import CoreModel, extract_metadata, Image

description = "Text to Image Generation Model"

class Inputs(CoreModel):
    prompt: str = Field(..., description="User text prompt")

class Params(CoreModel):
    pass

class Outputs(CoreModel):
    generated_image: Image = Field(..., description="AI Generated image described by user text prompt")

if __name__ == "__main__":
    extract_metadata(
                    Inputs, Params, Outputs,  # type: ignore
                    description, False
                )