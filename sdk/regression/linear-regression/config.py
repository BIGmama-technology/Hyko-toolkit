from pydantic import Field
from hyko_sdk.io import BaseModel
from hyko_sdk.metadata import MetaData, pmodel_to_ports
from typing import List

# Metadata

name = "Linear Regression"
description = "Predicts a future value based on historical data"
version = "1.0"
category = "Regression"
task = "Predict future value based on correleated data"

class Inputs(BaseModel):
    predict_x : float = Field(..., description="X axis value for which to predict Y axis value")

# Parameters to the function like temperature for gpt3. These values are constant in runtime
class Params(BaseModel):
    historical_x : List[float] = Field(..., description="Historical data of X axis")
    historical_y : List[float] = Field(..., description="Historical data of Y axis")

class Outputs(BaseModel):
    predict_y: float = Field(..., description="Predicted Y axis value")

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
