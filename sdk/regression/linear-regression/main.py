from config import Inputs, Outputs, Params
from fastapi import FastAPI, HTTPException, status
from sklearn.linear_model import LinearRegression
import numpy as np

app = FastAPI()

@app.post(
    "/load",
    response_model=None,
)
def load():
    pass

linear_regression = LinearRegression()

@app.post(
    "/",
    response_model=Outputs,
)
async def main(inputs: Inputs, params: Params):

    if len(params.historical_x) != len(params.historical_y):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Historical X and Y axises should have the same length",
        )

    X = np.array(params.historical_y).reshape(-1,1)
    Y = np.array(params.historical_y).reshape(-1,1)
    
    linear_regression.fit(X, Y)
    predict_y = linear_regression.predict([[inputs.predict_x]]) # type: ignore

    return Outputs(predict_y=predict_y) # type: ignore
