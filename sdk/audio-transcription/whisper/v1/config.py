from pydantic import Field
from hyko_sdk.utils import extract_metadata 
from hyko_sdk import CoreModel, Audio


description = "OpenAI's Audio Transcription model (Non API)"

class Inputs(CoreModel):
    audio: Audio = Field(..., description="Input audio that will be transcribed")

class Params(CoreModel):
    language: str = Field(default="en", description="the language of the audio")


class Outputs(CoreModel):
    transcribed_text: str = Field(..., description="Generated transcription text")



# dont change
if __name__ == "__main__":
    extract_metadata(
                    Inputs, Params, Outputs,  # type: ignore
                    description, False
                )