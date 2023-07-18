from pydantic import BaseModel, Field
from hyko_sdk.metadata import MetaData, pmodel_to_ports
from hyko_sdk.io import Image, String
# Metadata

name = "vit-gpt2-image-captioning"
description = "An image captioning model, gives a short description of the input image"
version = "1.0"
category = "Vision"

class Inputs(BaseModel):
    img : Image = Field(..., description="User inputted image to be captionned")

# Parameters to the function like temperature for gpt3. These values are constant in runtime
class Params(BaseModel):
    pass

class Outputs(BaseModel):
    text : String = Field(..., description="Caption of the image")

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
