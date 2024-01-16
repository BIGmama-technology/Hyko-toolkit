from pydantic import Field

from hyko_sdk.function import SDKFunction
from hyko_sdk.io import Audio
from hyko_sdk.metadata import CoreModel

func = SDKFunction(
    description="OpenAI's Audio Transcription model (Non API)",
)


@func.set_input
class Inputs(CoreModel):
    audio: Audio = Field(..., description="Input audio that will be transcribed")


@func.set_param
class Params(CoreModel):
    language: str = Field(default="en", description="The language of the audio")
    device_map: str = Field(..., description="Device map (Auto, CPU or GPU)")


@func.set_output
class Outputs(CoreModel):
    transcribed_text: str = Field(..., description="Generated transcription text")
