from pydantic import BaseModel
from sdk.common.metadata import MetaData, pmodel_to_ports

# Change Meta data here:#####################

name = "Divide"
description = "Divide two numbers (a/b)"
version = "1.0"
category = "Math"

##############################################


# Change types of inputs and outputs here:#####################

# main inputs to the function like a prompt for gpt3. These values are dynamic in runtime.
class Inputs(BaseModel):
    a: float
    b: float


# runtime means when the prototype is generated and deployed for the user (ui and all)


# Parameters to the function like temperature for gpt3. These values are constant  n runtime
class Params(BaseModel):
    pass


# outputs of the function.
class Outputs(BaseModel):
    result: float


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
    print(__meta_data__.json())
