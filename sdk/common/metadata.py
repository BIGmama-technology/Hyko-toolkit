from pydantic import BaseModel
from sdk.common.io import IOPort


def pmodel_to_json(pmodel: BaseModel) -> list[IOPort]:
    d = pmodel.__fields__
    arr = []
    for k, v in d.items():
        arr.append(IOPort(name=k, type=v.type_.__name__.upper()))

    return arr


class MetaData(BaseModel):
    name: str
    description: str
    version: str
    category: str
    inputs: list[IOPort]
    outputs: list[IOPort]
    params: list[IOPort]
