from pydantic import Field
from hyko_sdk.io import BaseModel
from hyko_sdk.metadata import MetaData, pmodel_to_ports
from typing import List

#THe metadata
name ="paragraph_to_sentence_splitter"
description = " Takes a paragraph and tokenizes (splits) it into a list of sentences"
version = "1.0"
category = "NLP"


#main inputs of the function
class Inputs(BaseModel):
    pass

#============

#Parameters of the function
class Params(BaseModel):
    first : str = Field(..., description="paragraph")

#outputs of the functions
class Outputs(BaseModel):
    output : List[str] = Field(..., descriptions="sentences")

# Function metadata

__meta_date__ = MetaData(
    name= name,
    description = description,
    version = version,
    category = category,
    inptus = pmodel_to_ports(Inputs),
    params = pmodel_to_ports(Params),
    outputs = pmodel_to_ports(Outputs),
    requires_gpu = False,
)
if __name__== "__main__" :
    print(__meta_date__.json(indent=2))
