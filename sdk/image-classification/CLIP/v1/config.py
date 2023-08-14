from pydantic import Field
from hyko_sdk import Image, CoreModel, extract_metadata
from typing import List

description = """
Classify an image to one class out of the list of classes. 
Example: if the classes are ['cat', 'dog'] then the model will have to choose if the image is either a cat or dog
"""

class Inputs(CoreModel):
    img: Image = Field(..., description="Image input by user to be classified")

class Params(CoreModel):
    classes: List[str] = Field(..., description="List of classes to classify the input image on")

class Outputs(CoreModel):
    output_class: str = Field(..., description="The class of the image")


if __name__ == "__main__":
    extract_metadata(
                    Inputs, Params, Outputs,  # type: ignore
                    description, False
                )
