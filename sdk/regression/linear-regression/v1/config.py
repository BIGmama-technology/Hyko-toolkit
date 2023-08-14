from pydantic import Field
from hyko_sdk import CoreModel, extract_metadata
from typing import List

description = "Predicts a future value based on historical data"

class Inputs(CoreModel):
    predict_x : float = Field(..., description="X axis value for which to predict Y axis value")

class Params(CoreModel):
    historical_x : List[float] = Field(..., description="Historical data of X axis")
    historical_y : List[float] = Field(..., description="Historical data of Y axis")

class Outputs(CoreModel):
    predict_y: float = Field(..., description="Predicted Y axis value")

if __name__ == "__main__":
    extract_metadata(
                    Inputs, Params, Outputs,  # type: ignore
                    description, False
                )