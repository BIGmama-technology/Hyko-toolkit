from pydantic import BaseModel
import fastapi


app = fastapi.FastAPI() 




# Change types of inputs and outputs here:#####################

# main inputs to the function like a prompt for gpt3. These values are dynamic in runtime.
class Inputs(BaseModel):
    a: float
    b: float

# runtime means when the prototype is generated and deployed for the user (ui and all)

# Parameters to the function like temperature for gpt3. These values are constant  n runtime
class Params(BaseModel):
    pass

# outputs of the function.
class Outputs(BaseModel):
    result: float


#################################################################

# Insert the main code of the function here #################################################################

# keep the decorator, function declaration and return type the same. 
# the main function should always take Inputs as the first argument and Params as the second argument.
# should always return Outputs.
@app.post("/", response_model=Outputs)
async def main(inputs: Inputs, params: Params):
   
    return Outputs(result=inputs.a + inputs.b)

##############################################################################################################

# Change Meta data here:#####################

name = "Add"
description = "Add two numbers together"
version = "1.0"
category = "Math"

##############################################




# Keep the same


def pmodel_to_json(pmodel: BaseModel):
    d = pmodel.__fields__
    arr = []
    for _,v in d.items():
        arr.append(str(v.type_))

    return arr


class MetaData(BaseModel):
    name: str
    description: str
    version: str
    category: str
    inputs: list[str]
    outputs: list[str]
    params: list[str]

@app.get("/metadata", response_model=MetaData)
async def metadata():
    inputs = pmodel_to_json(Inputs)
    outputs = pmodel_to_json(Outputs)
    params = pmodel_to_json(Params)

    return MetaData(
        name=name,
        description=description, 
        version=version,
        category=category,
        inputs=inputs, 
        outputs=outputs, 
        params=params
    )
