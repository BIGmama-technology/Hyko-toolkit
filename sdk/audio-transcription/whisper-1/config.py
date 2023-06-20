from typing import Optional
from pydantic import BaseModel, Field
from sdk.common.io import Number, String, Audio
from sdk.common.metadata import MetaData, pmodel_to_ports

# Change Meta data here:#####################

name = "whisper-1"
description = "OpenAI's Audio transcription"
version = "1.0"
category = "OpenAi"

##############################################


# Change types of inputs and outputs here:#####################

# main inputs to the function like a prompt for gpt3. These values are dynamic in runtime.
class Inputs(BaseModel):
    audio: Audio = Field(..., description="User audio input to be transcribed")
    prompt: Optional[String] = Field(..., description="User additional text prompt")
    language: Optional[String] = Field(..., description="User specified language")



# runtime means when the prototype is generated and deployed for the user (ui and all)


# Parameters to the function like temperature for gpt3. These values are constant  n runtime
class Params(BaseModel):
    api_key: String = Field(..., description="OpenAI's API KEY")
    temperature: Optional[Number] = Field(..., description="Whisper's temperature")


# outputs of the function.
class Outputs(BaseModel):
    transcript: String = Field(..., description="Transcript of the audio inputted by the user")


# Function metadata, should always be here

__meta_data__ = MetaData(
    name=name,
    description=description,
    version=version,
    category=category,
    inputs=pmodel_to_ports(Inputs), # type: ignore
    params=pmodel_to_ports(Params), # type: ignore
    outputs=pmodel_to_ports(Outputs), # type: ignore
)


if __name__ == "__main__":
    print(__meta_data__.json(indent=2))