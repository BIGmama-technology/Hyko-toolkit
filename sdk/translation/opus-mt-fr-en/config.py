from pydantic import BaseModel, Field
from hyko_sdk.metadata import MetaData, pmodel_to_ports
from hyko_sdk.io import String, Audio
from typing import List
# Metadata

name = "opush-mt-fr-en"
description = "OPUS French to English Translation specialized model"
version = "1.0"
category = "Translation"
# task = "Translation"


class Inputs(BaseModel):
    french_text: String = Field(..., description="French text")


# Parameters to the function like temperature for gpt3. These values are constant  n runtime
class Params(BaseModel):
    pass


class Outputs(BaseModel):
    english_translated_text: String = Field(..., description="English translated text")



# Function metadata, should always be here

__meta_data__ = MetaData(
    name=name,
    description=description,
    version=version,
    category=category,
    inputs=pmodel_to_ports(Inputs),  # type: ignore
    params=pmodel_to_ports(Params),  # type: ignore
    outputs=pmodel_to_ports(Outputs),  # type: ignore
)

if __name__ == "__main__":
    print(__meta_data__.json(indent=2))