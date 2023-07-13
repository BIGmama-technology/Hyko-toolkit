from typing import Optional
from pydantic import BaseModel, Field
from hyko_sdk.io import Number, Integer, String
from hyko_sdk.metadata import MetaData, pmodel_to_ports

# Change Meta data here:#####################

name = "text-davinci-003"
description = "OpenAI's Text completion model"
version = "1.0"
category = "OpenAi"

##############################################


# Change types of inputs and outputs here:#####################

# main inputs to the function like a prompt for gpt3. These values are dynamic in runtime.
class Inputs(BaseModel):
    prompt: String = Field(..., description="User text prompt")



# runtime means when the prototype is generated and deployed for the user (ui and all)


# Parameters to the function like temperature for gpt3. These values are constant  n runtime
class Params(BaseModel):
    system_prompt: String = Field(default=None, description='System prompt for the model')
    api_key: String = Field(..., description="OpenAI's API KEY")
    max_tokens: Optional[Integer] = Field(default=100, description="maximum number of tokens generated by the LLM")
    temperature: Optional[Number] = Field(default=0.6, description="GPT3 temperature")
    top_p: Optional[Number] = Field(default=0.6, description="GPT3 Top P")


# outputs of the function.
class Outputs(BaseModel):
    generated_text: String = Field(..., description="Generated text by GPT3")


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
