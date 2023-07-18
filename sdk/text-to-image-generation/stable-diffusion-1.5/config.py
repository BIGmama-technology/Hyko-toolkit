from pydantic import Field
from hyko_sdk.metadata import MetaData, pmodel_to_ports
from hyko_sdk.io import Image, BaseModel
# Metadata

name = "Stable Diffusion 1.5"
description = "Text to image generation model"
version = "1.0"
category = "Vision"

class Inputs(BaseModel):
    input_prompt : str = Field(..., description="User prompt to generate an from")

# Parameters to the function like temperature for gpt3. These values are constant  n runtime
class Params(BaseModel):
    pass

class Outputs(BaseModel):
    generated_image : Image = Field(..., description="Generated Image based on user input prompt")

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
