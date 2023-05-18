import fastapi
from example.utils import pmodel_to_json
from pydantic import BaseModel

app = fastapi.FastAPI()

class MetaData(BaseModel):
    name: str
    description: str
    version: str
    category: str
    inputs: List[str]
    inputs_descr: str
    outputs: List[str]
    outputs_descr: str
    params: List[str]

######################################################
################### Model Metadata ###################
######################################################
name = ""
description = ""
version = ""
category = ""
inputs_descr=""
outputs_descr=""

######################################################
################### Model inputs #####################
######################################################
class Inputs(BaseModel):
    pass

######################################################
################### Model params #####################
######################################################
class Params(BaseModel):
    pass


######################################################
################### Model output #####################
######################################################
class Outputs(BaseModel):
    pass


######################################################
################### Main function ####################
######################################################
@app.post("/", response_model=Outputs)
async def main(inputs: Inputs, params: Params):
    return Outputs()




def pmodel_to_json(pmodel: BaseModel):
    d = pmodel.__fields__
    arr = []
    for _, v in d.items():
        arr.append(str(v.type_.__name__))
    return arr

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
        inputs_descr=inputs_descr,
        outputs=outputs,
        outputs_descr=outputs_descr,
        params=params,
    )