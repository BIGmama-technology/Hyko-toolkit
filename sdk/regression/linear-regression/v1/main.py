from typing import List

import numpy as np
from fastapi.exceptions import HTTPException
from pydantic import Field
from sklearn.linear_model import LinearRegression

from hyko_sdk.function import SDKFunction
from hyko_sdk.metadata import CoreModel

func = SDKFunction(
    description="Predicts a future value based on historical data",
    requires_gpu=False,
)


class Inputs(CoreModel):
    predict_x: float = Field(
        ..., description="X axis value for which to predict Y axis value"
    )


class Params(CoreModel):
    historical_x: List[float] = Field(..., description="Historical data of X axis")
    historical_y: List[float] = Field(..., description="Historical data of Y axis")


class Outputs(CoreModel):
    predict_y: float = Field(..., description="Predicted Y axis value")


linear_regression = LinearRegression()


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    if len(params.historical_x) != len(params.historical_y):
        raise HTTPException(
            status_code=500,
            detail="Historical X and Y axises should have the same length",
        )

    x = np.array(params.historical_y).reshape(-1, 1)
    y = np.array(params.historical_y).reshape(-1, 1)

    linear_regression.fit(x, y)
    predict_y = linear_regression.predict([[inputs.predict_x]])  # type: ignore

    return Outputs(predict_y=predict_y)  # type: ignore
