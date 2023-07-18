from pydantic import BaseModel, Field
from hyko_sdk.metadata import MetaData, pmodel_to_ports
from hyko_sdk.io import Audio

# Metadata

name = "Whisper"
description = "OpenAI's Audio Transcription (Non API)"
version = "1.0"
category = "Speech recognition"
task = "Speech to text translation"


class Inputs(BaseModel):
    input_audio: Audio = Field(..., description="Audio to be transcribed")


# Parameters to the function like temperature for gpt3. These values are constant  n runtime
class Params(BaseModel):
    pass


class Outputs(BaseModel):
    transcript: str = Field(..., description="Transcription")


# Function metadata, should always be here

__meta_data__ = MetaData(
    name=name,
    description=description,
    version=version,
    category=category,
    inputs=pmodel_to_ports(Inputs),  # type: ignore
    params=pmodel_to_ports(Params),  # type: ignore
    outputs=pmodel_to_ports(Outputs),  # type: ignore
    requires_gpu=True,
)

if __name__ == "__main__":
    print(__meta_data__.json(indent=2))