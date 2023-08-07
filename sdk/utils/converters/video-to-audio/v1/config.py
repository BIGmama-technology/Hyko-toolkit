from pydantic import Field
from hyko_sdk import CoreModel, extract_metadata, Video, Audio

description = "Convert a video type to audio type (takes only the audio data)"

class Inputs(CoreModel):
    video: Video = Field(..., description="User input video to be converted to audio")

class Params(CoreModel):
    pass

class Outputs(CoreModel):
    audio: Audio = Field(..., description="converted audio")


if __name__ == "__main__":
    extract_metadata(
                    Inputs, Params, Outputs,  # type: ignore
                    description, False
                )