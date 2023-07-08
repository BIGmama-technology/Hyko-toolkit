from pydantic import BaseModel, Field
from hyko_sdk.metadata import MetaData, pmodel_to_ports
from hyko_sdk.io import Image, String
from typing import List
# Metadata

name = "owlvit-base-patch32"
description = "Zero-shot object detection/recogntion model by Google"
version = "1.0"
category = "Visual-Recognition/Detection"

class Inputs(BaseModel):
    # tags : List[String] = Field(..., description="List of object(s) names to be detected")
    img : Image = Field(..., description="Input Image")
    tags : List[String] = Field(..., description="List of object(s) names to be detected")

# Parameters to the function like temperature for gpt3. These values are constant  n runtime
class Params(BaseModel):
    pass

class Outputs(BaseModel):
    output_image: Image = Field(..., description="Input image + detection bounding Boxes")

# Function metadata, should always be here

__meta_data__ = MetaData(
    name=name,
    description=description,
    version=version,
    category=category,
    inputs=pmodel_to_ports(Inputs), # type: ignore
    params=pmodel_to_ports(Params), # type: ignore
    outputs=pmodel_to_ports(Outputs), # type: ignore
)


if __name__ == "__main__":
    print(__meta_data__.json(indent=2))
