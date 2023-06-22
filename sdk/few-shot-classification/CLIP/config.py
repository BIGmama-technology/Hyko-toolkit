from pydantic import BaseModel
from sdk.common.metadata import MetaData, pmodel_to_ports
from sdk.common.io import Image, String
from typing import Union, List

# Metadata

name = "clip-vit-large-patch14"
description = "CLIP Model, few shot image classification"
version = "1.0"
category = "Image Classificatoin"
task = "Classifies Image content to one of items in List[classes : list[str]]"


class Inputs(BaseModel):
    img: Image
    classes: List[String]


# Parameters to the function like temperature for gpt3. These values are constant  n runtime
class Params(BaseModel):
    pass


class Outputs(BaseModel):
    probs: List[float]

# Function metadata, should always be here

__meta_data__ = MetaData(
    name=name,
    description=description,
    version=version,
    category=category,
    task=task,
    inputs=pmodel_to_ports(Inputs),  # type: ignore
    params=pmodel_to_ports(Params),  # type: ignore
    outputs=pmodel_to_ports(Outputs),  # type: ignore
)
