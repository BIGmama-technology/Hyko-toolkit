from pydantic import BaseModel
from sdk.common.metadata import MetaData, pmodel_to_json

# Change Meta data here:#####################

name = "OpenAi completion (text-davinci-003)"
description = "OpenAi (text-davinci-003)"
version = "1.0"
category = "OpenAi"

##############################################


# Change types of inputs and outputs here:#####################

# main inputs to the function like a prompt for gpt3. These values are dynamic in runtime.
class Inputs(BaseModel):
    prompt: str
    api_key: str
    max_tokens: float
    temperature: float
    top_p: float


# runtime means when the prototype is generated and deployed for the user (ui and all)


# Parameters to the function like temperature for gpt3. These values are constant  n runtime
class Params(BaseModel):
    pass


# outputs of the function.
class Outputs(BaseModel):
    generated_text: str


# Function metadata, should always be here

__meta_data__ = MetaData(
    name=name,
    description=description,
    version=version,
    category=category,
    inputs=pmodel_to_json(Inputs),
    params=pmodel_to_json(Params),
    outputs=pmodel_to_json(Outputs),
)


if __name__ == "__main__":
    print(__meta_data__.json())
