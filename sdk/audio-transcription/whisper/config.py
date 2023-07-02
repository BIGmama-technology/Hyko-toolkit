from pydantic import BaseModel
from hyko_sdk.metadata import MetaData, pmodel_to_ports
from hyko_sdk.io import String, Audio
from typing import List

# Metadata

name = "Whisper"
description = "OpenAI's Audio Transcription (Non API)"
version = "1.0"
category = "Speech recognition"
task = "Speech to text translation"


class Inputs(BaseModel):
    input_audio: Audio


# Parameters to the function like temperature for gpt3. These values are constant  n runtime
class Params(BaseModel):
    pass


class Outputs(BaseModel):
    output_text: str


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
