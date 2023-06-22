from pydantic import BaseModel, Field
from hyko_sdk.metadata import MetaData, pmodel_to_ports
from hyko_sdk.io import Image
# Metadata

name = "vit-gpt2-image-captioning"
description = "An image captioning model"
version = "1.0"
category = "Vision"

class Inputs(BaseModel):
    img : Image = Field(..., description="User inputted image to be captionned")

# Parameters to the function like temperature for gpt3. These values are constant  n runtime
class Params(BaseModel):
    pass

class Outputs(BaseModel):
    text : str = Field(..., description="Caption of the image inputted by the user")

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
