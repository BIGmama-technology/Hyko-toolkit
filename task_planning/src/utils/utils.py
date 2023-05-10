import json
from pydantic import BaseModel
from typing import List

def save_json(filename, json_data):
    with open(filename, "w") as f:
        json.dump(json_data, f)

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