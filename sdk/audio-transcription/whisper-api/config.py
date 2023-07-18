from typing import Optional
from pydantic import BaseModel, Field
from hyko_sdk.io import Number, String, Audio
from hyko_sdk.metadata import MetaData, pmodel_to_ports

# Change Meta data here:#####################

name = "Whisper (API)"
description = "OpenAI's Audio Transcription model (API)"
version = "1.0"
category = "Audio Transcription"
task = "Speech to text transcription"

##############################################


# Change types of inputs and outputs here:#####################

# main inputs to the function like a prompt for gpt3. These values are dynamic in runtime.
class Inputs(BaseModel):
    audio: Audio = Field(..., description="User audio input to be transcribed")


# Parameters to the function like temperature for gpt3. These values are constant  n runtime
class Params(BaseModel):
    prompt: Optional[String] = Field(default=None, description="User additional text prompt for the model")
    language: Optional[String] = Field(default='en', description="ISO-639-1 transcription language")
    api_key: String = Field(..., description="OpenAI's API KEY")
    temperature: Optional[Number] = Field(default=None, description="Whisper model temperature")


# outputs of the function.
class Outputs(BaseModel):
    transcribed_text: String = Field(..., description="Generated transcription text")


# Function metadata, should always be here

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


if __name__ == "__main__":
    print(__meta_data__.json(indent=2))
