from pydantic import BaseModel, Field
from hyko_sdk.metadata import MetaData, pmodel_to_ports
from hyko_sdk.io import Image, String
from typing import List

# Metadata

name = "clip-vit-large-patch14"
description = """
Classify an image to one class out of the user-inputted list of classes. 
Example: if the classes are ['cat', 'dog'] then the model will have to choose if the image is a cat or dog
"""

version = "1.0"
category = "Image Classification"


class Inputs(BaseModel):
    img: Image = Field(..., description="Image input by user to be classified")


# Parameters to the function like temperature for gpt3. These values are constant  n runtime
class Params(BaseModel):
    classes: List[String] = Field(..., description="List of classes to classify the input image on")


class Outputs(BaseModel):
    output_class: String = Field(..., description="The class of the image")
# Function metadata, should always be here

__meta_data__ = MetaData(
    name=name,
    description=description,
    version=version,
    category=category,
    inputs=pmodel_to_ports(Inputs),  # type: ignore
    params=pmodel_to_ports(Params),  # type: ignore
    outputs=pmodel_to_ports(Outputs),  # type: ignore
    requires_gpu=True,
)

if __name__ == "__main__":
    print(__meta_data__.json(indent=2))
