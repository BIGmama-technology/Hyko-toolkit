from pydantic import Field
from hyko_sdk.metadata import MetaData, pmodel_to_ports
from hyko_sdk.io import String, Audio, BaseModel


# Metadata
name = "Whisper"
description = "OpenAI's Audio Transcription model (Non API)"
version = "1.0"
category = "Audio Transcription"
task = "Speech to text transcription"


class Inputs(BaseModel):
    audio: Audio = Field(..., description="Input audio that will be transcribed")


# Parameters to the function like temperature for gpt3. These values are constant in runtime
class Params(BaseModel):
    pass


class Outputs(BaseModel):
    transcribed_text: String = Field(..., description="Generated transcription text")


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