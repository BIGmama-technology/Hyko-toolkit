import fastapi
from .config import Inputs, Params, Outputs
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import pandas as pd
from typing import List, Tuple, Union
from sklearn.linear_model import LinearRegression
import random
app = fastapi.FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#################################################################

# Insert the main code of the function here #################################################################
data_ = pd.read_csv("/sdk/function/Datasheet.csv")
bio_ = data_["biobrikcs demand"]
standard = data_['B12 demand']
months = data_["mois"]

randomness = {}
randomness_2 = {}

for i in range(10000):
    randomness[i] = int(random.random() * 10)

for i in range(10000):
    randomness_2[i] = int(random.random() * 10)

months = np.arange(bio_.size).reshape(-1,1)
standard = np.array(standard).reshape(-1,1)
bio_ = np.array(bio_).reshape(-1,1)

class prod_regression:
    bio_model : LinearRegression = LinearRegression()
    standard_model : LinearRegression = LinearRegression()
    def __init__(self, bio_data : np.ndarray = None,
                 standard_data : np.ndarray = None,
                 time_ : np.ndarray = None):
        self.bio_model.fit(time_, bio_data)
        self.standard_model.fit(time_, standard_data)
    def predict(self, month : int, day: int) -> Tuple[float, float]:
        bio_pred = self.bio_model.predict(month)
        standard_pred = self.standard_model.predict(month)
        bio_pred += randomness[day + month * 12]
        standard_pred += randomness_2[day + month * 12]

        return bio_pred, standard_pred
    def __call__(self, month: int = None) -> dict:
        pass
# keep the decorator, function declaration and return type the same.
# the main function should always take Inputs as the first argument and Params as the second argument.
# should always return Outputs.

model = prod_regression(bio_, standard, months)

@app.post("/", response_model=Outputs)
async def main(inputs: Inputs):
    print(inputs)
    bio, standard = model.predict([[inputs.month_in_the_future]])

    return Outputs(standard_bricks_production=standard, bio_bricks_production=bio)


##############################################################################################################

