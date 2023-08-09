from pydantic import Field
from hyko_sdk.io import BaseModel
from hyko_sdk.metadata import MetaData, pmodel_to_ports
from typing import List

name = "top_similar_sentences"
description = "Takes a list of sentences and a query sentences and returns the top_k most similar sentences to the query"
version = "1.0"
category = "NLP"

###########################################

#main inputs 
class Inputs(BaseModel):
    pass


#Parameters to the function
class Params(BaseModel):
    first : List[str] = Field(..., descriptions = "search_documents")
    second : str = Field(..., description = "query")
    third : int = Field(default = 5, description = "top_k")

#Outputs of the function
class Outputs(BaseModel):
    output : List[str]= Field(..., description= "list of top elected sentences")


#function metadate
__meta_data__ = MetaData(
    name=name,
    description=description,
    version=version,
    category=category,
    inputs=pmodel_to_ports(Inputs), # type: ignore
    params=pmodel_to_ports(Params), # type: ignore
    outputs=pmodel_to_ports(Outputs), # type: ignore
    requires_gpu=False,
)