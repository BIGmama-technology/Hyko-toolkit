from pydantic import BaseModel
from sdk.common.io import Image
from sdk.common.metadata import MetaData, pmodel_to_ports
# Metadata

name = "SegFormer"
description = "Image Segmentation Model"
version = "1.0"
category = "Vision"

class Inputs(BaseModel):
    img : Image

# Parameters to the function like temperature for gpt3. These values are constant  n runtime
class Params(BaseModel):
    pass

class Outputs(BaseModel):
    img : Image

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
