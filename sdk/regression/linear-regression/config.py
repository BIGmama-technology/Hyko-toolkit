from pydantic import BaseModel
from hyko_sdk.metadata import MetaData, pmodel_to_ports
from hyko_sdk.io import String, Audio
from typing import List, Union
import numpy as np

# Metadata

name = "Linear Regressoin"
description = "Linear Regression: Predicts future values of unseen samples on the X axis"
version = "1.0"
category = "Prediction"
task = "Predict future value based on correleated data"

class Inputs(BaseModel):
    input_sample : Union[float, int]

# Parameters to the function like temperature for gpt3. These values are constant  n runtime
class Params(BaseModel):
    input_x : List[Union[float, int]]
    input_y : List[Union[float, int]]

class Outputs(BaseModel):
    prediction: Union[float, int]

# Function metadata, should always be here

__meta_data__ = MetaData(
    name=name,
    description=description,
    version=version,
    category=category,
    task=task,
    inputs=pmodel_to_ports(Inputs),  # type: ignore
    params=pmodel_to_ports(Params),  # type: ignore
    outputs=pmodel_to_ports(Outputs),  # type: ignore
)
