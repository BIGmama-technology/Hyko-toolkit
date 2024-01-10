import numpy as np
from fastapi.exceptions import HTTPException
from metadata import Inputs, Outputs, Params, func
from sklearn.linear_model import LinearRegression

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
