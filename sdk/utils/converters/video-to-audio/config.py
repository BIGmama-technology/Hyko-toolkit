from pydantic import BaseModel, Field
from hyko_sdk.io import Video, Audio
from hyko_sdk.metadata import MetaData, pmodel_to_ports

# Change Meta data here:#####################

name = "Video to Audio"
description = "Convert a video type to audio type (takes only the audio data)"
version = "1.0"
category = "utils/converters"

##############################################


# Change types of inputs and outputs here:#####################

# main inputs to the function like a prompt for gpt3. These values are dynamic in runtime.
class Inputs(BaseModel):
    video: Video = Field(..., description="User input video to be converted to audio")

# runtime means when the prototype is generated and deployed for the user (ui and all)


# Parameters to the function like temperature for gpt3. These values are constant  n runtime
class Params(BaseModel):
    pass


# outputs of the function.
class Outputs(BaseModel):
    audio: Audio = Field(..., description="converted audio")


# Function metadata, should always be here

__meta_data__ = MetaData(
    name=name,
    description=description,
    version=version,
    category=category,
    inputs=pmodel_to_ports(Inputs), # type: ignore
    params=pmodel_to_ports(Params), # type: ignore
    outputs=pmodel_to_ports(Outputs), # type: ignore
    requires_gpu=False
)


if __name__ == "__main__":
    print(__meta_data__.json(indent=2))
