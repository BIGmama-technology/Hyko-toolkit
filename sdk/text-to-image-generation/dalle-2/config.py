from pydantic import Field
from hyko_sdk.io import Image, BaseModel
from hyko_sdk.metadata import MetaData, pmodel_to_ports

# Change Meta data here:#####################

name = "dalle-2"
description = "OpenAI's Image generation from text prompt"
version = "1.0"
category = "OpenAi"

##############################################


# Change types of inputs and outputs here:#####################

# main inputs to the function like a prompt for gpt3. These values are dynamic in runtime.
class Inputs(BaseModel):
    prompt: str = Field(..., description="User text prompt")


# runtime means when the prototype is generated and deployed for the user (ui and all)


# Parameters to the function like temperature for gpt3. These values are constant  n runtime
class Params(BaseModel):
    api_key: str = Field(..., description="OpenAI's API KEY")


# outputs of the function.
class Outputs(BaseModel):
    generated_image: Image = Field(..., description="AI Generated image described by user text prompt")


# Function metadata, should always be here

__meta_data__ = MetaData(
    name=name,
    description=description,
    version=version,
    category=category,
    inputs=pmodel_to_ports(Inputs), # type: ignore
    params=pmodel_to_ports(Params), # type: ignore
    outputs=pmodel_to_ports(Outputs), # type: ignore
    requires_gpu=False
)


if __name__ == "__main__":
    print(__meta_data__.json(indent=2))
