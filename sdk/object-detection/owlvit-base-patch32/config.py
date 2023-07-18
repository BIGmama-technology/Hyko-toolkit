from pydantic import Field
from hyko_sdk.metadata import MetaData, pmodel_to_ports
from hyko_sdk.io import Image, BaseModel
from typing import List
# Metadata

name = "owlvit-base-patch32"
description = "Object detection/recogntion model, draws bounding boxes over the image if the object is in the list of tags."
version = "1.0"
category = "Visual-Recognition/Detection"

class Inputs(BaseModel):
    # tags : List[String] = Field(..., description="List of object(s) names to be detected")
    img : Image = Field(..., description="Input Image")

# Parameters to the function like temperature for gpt3. These values are constant  n runtime
class Params(BaseModel):
    tags : List[str] = Field(..., description="List of object(s) names to be detected")

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
    requires_gpu=True,
)


if __name__ == "__main__":
    print(__meta_data__.json(indent=2))
