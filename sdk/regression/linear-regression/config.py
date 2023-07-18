from pydantic import BaseModel, Field
from hyko_sdk.metadata import MetaData, pmodel_to_ports
from hyko_sdk.io import Number
from typing import List, Union
import numpy as np

# Metadata

name = "Linear Regression"
description = "Linear Regression: Predicts future values of unseen samples on the X axis"
version = "1.0"
category = "Regression"
task = "Predict future value based on correleated data"

class Inputs(BaseModel):
    input_sample : Number = Field(..., description="Input sample of X axis to get a prediction on for Y axis")

# Parameters to the function like temperature for gpt3. These values are constant in runtime
class Params(BaseModel):
    input_x : List[Number] = Field(..., description="Data of X axis")
    input_y : List[Number] = Field(..., description="Data of Y axis")

class Outputs(BaseModel):
    prediction: Number = Field(..., description="Predicted value of Y axis")

# Function metadata, should always be here

__meta_data__ = MetaData(
    name=name,
    description=description,
    version=version,
    category=category,
    inputs=pmodel_to_ports(Inputs),  # type: ignore
    params=pmodel_to_ports(Params),  # type: ignore
    outputs=pmodel_to_ports(Outputs),  # type: ignore
    requires_gpu=False
)

if __name__ == "__main__":
    print(__meta_data__.json(indent=2))
