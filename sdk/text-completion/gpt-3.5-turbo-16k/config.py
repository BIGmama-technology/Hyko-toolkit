from typing import Optional
from pydantic import Field
from hyko_sdk.io import BaseModel
from hyko_sdk.metadata import MetaData, pmodel_to_ports

# Change Meta data here:#####################

name = "gpt-3.5-turbo-16k"
description = "OpenAI's GPT 3.5 Turbo Large completion model (API)"
version = "1.0"
category = "OpenAi"
task = "Text Completion"

##############################################


# Change types of inputs and outputs here:#####################

# main inputs to the function like a prompt for gpt3. These values are dynamic in runtime.
class Inputs(BaseModel):
    prompt: str = Field(..., description="Input prompt (16k tokens max context size)")



# runtime means when the prototype is generated and deployed for the user (ui and all)


# Parameters to the function like temperature for gpt3. These values are constant  n runtime
class Params(BaseModel):
    system_prompt: Optional[str] = Field(default=None, description='System prompt for the model (used to instruct the model)')
    api_key: str = Field(..., description="OpenAI's API KEY")
    max_tokens: Optional[int] = Field(default=None, description="Maximum number of tokens generated by the model")
    temperature: Optional[float] = Field(default=None, description="Model's temperature")
    top_p: Optional[float] = Field(default=None, description="Model's Top P")


# outputs of the function.
class Outputs(BaseModel):
    completion_text: str = Field(..., description="Completion text")


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
