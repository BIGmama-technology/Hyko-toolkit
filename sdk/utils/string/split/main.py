import fastapi
from config import Inputs, Params, Outputs, String

app = fastapi.FastAPI()

app = fastapi.FastAPI()

@app.post("/load", response_model=None)
def load():
    pass

@app.post("/", response_model=Outputs)
async def main(inputs: Inputs, params: Params):
    res = []
    for s in inputs.text.split(params.delimeter):
        res.append(String(s))
    return Outputs(splitted=res)


##############################################################################################################

