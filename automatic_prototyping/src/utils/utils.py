import json
from pydantic import BaseModel
from typing import List

def save_json(filename, json_data):
    with open(filename, "w") as f:
        json.dump(json_data, f)

def read_json(filename):
    with open(filename, "r") as f:
        data = json.load(f)
    return data

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