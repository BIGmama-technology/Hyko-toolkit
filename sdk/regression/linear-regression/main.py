from config import Inputs, Outputs, Params, Number
import fastapi
from sklearn.linear_model import LinearRegression
import numpy as np

app = fastapi.FastAPI()
@app.post("/load", response_model=None)
def load():
    pass
linear_regression = LinearRegression()

@app.post("/", response_model=Outputs)
async def main(inputs: Inputs, params: Params):
    assert len(params.input_x) == len(params.input_y), "X and Y lists are of different Lengths"
    
    X = np.array(params.input_x).reshape(-1,1)
    Y = np.array(params.input_y).reshape(-1,1)
    
    linear_regression.fit(X, Y)
    output = linear_regression.predict([[inputs.input_sample]])

    return Outputs(prediction=Number(output))
