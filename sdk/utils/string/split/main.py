import fastapi
from config import Inputs, Params, Outputs, String

app = fastapi.FastAPI()

#################################################################

# Insert the main code of the function here #################################################################


# keep the decorator, function declaration and return type the same.
# the main function should always take Inputs as the first argument and Params as the second argument.
# should always return Outputs.
@app.post("/", response_model=Outputs)
async def main(inputs: Inputs, params: Params):
    res = []
    for s in inputs.text.split(params.delimeter):
        res.append(String(s))
    return Outputs(splitted=res)


##############################################################################################################

