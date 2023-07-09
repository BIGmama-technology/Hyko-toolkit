from pydantic import BaseModel, Field
from hyko_sdk.metadata import MetaData, pmodel_to_ports
from hyko_sdk.io import Image
# Metadata

name = "falcon-7B"
description = "instruct generation model"
version = "1.0"
category = "text-LLM"

class Inputs(BaseModel):
    input_prompt : str = Field(..., description="User prompt to falcon-instruct")

# Parameters to the function like temperature for gpt3. These values are constant  n runtime
class Params(BaseModel):
    pre_prompt : str = Field(default=None, describtion = "Pre-prompt or pre-instruction to falcon-instruct")
    max_length : int = Field(default = 200, description= "Max tokens to generate")
    do_sample : bool = Field(default=True,description= "Sample instrad of greedy decoding")
    top_k : int = Field(default=10,description="top_k candidates for each token generation")
    num_return_sequences : int = Field(defualt=1, description="Number of sequences to return")

class Outputs(BaseModel):
    generated_text : str = Field(..., description="Generated Text from falcon-instruct")

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
