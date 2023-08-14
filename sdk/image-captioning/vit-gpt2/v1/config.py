from pydantic import Field
from hyko_sdk import extract_metadata, Image, CoreModel

description = "An image captioning model, gives a short description of the input image"

class Inputs(CoreModel):
    image : Image = Field(..., description="User inputted image to be captionned")

# Parameters to the function like temperature for gpt3. These values are constant in runtime
class Params(CoreModel):
    pass

class Outputs(CoreModel):
    image_description : str = Field(..., description="description/caption of the image")

if __name__ == "__main__":
    extract_metadata(
                    Inputs, Params, Outputs,  # type: ignore
                    description, False
                )