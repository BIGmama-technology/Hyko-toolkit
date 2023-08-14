from fastapi import FastAPI
from config import Inputs, Params, Outputs

app = FastAPI()

@app.post(
    "/load",
    response_model=None,
)
def load():
    pass

@app.post(
    "/",
    response_model=Outputs,
)
async def main(inputs: Inputs, params: Params):
    return Outputs(splitted=inputs.text.split(params.delimeter))


##############################################################################################################

