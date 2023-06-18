from pydantic import BaseModel
from sdk.common.metadata import MetaData, pmodel_to_ports
from sdk.common.io import Image
# Metadata

name = "Addvit-gpt2-image-captioning"
description = "This is an image captioning model "
version = "1.0"
category = "Vision"
task = "Image Captioning"

class Inputs(BaseModel):
    img : Image

# Parameters to the function like temperature for gpt3. These values are constant  n runtime
class Params(BaseModel):
    pass

class Outputs(BaseModel):
    text : str

# Function metadata, should always be here

__meta_data__ = MetaData(
    name=name,
    description=description,
    version=version,
    category=category,
    task=task,
    inputs=pmodel_to_ports(Inputs), # type: ignore
    params=pmodel_to_ports(Params), # type: ignore
    outputs=pmodel_to_ports(Outputs), # type: ignore
)
