from typing import Optional

from pydantic import Field

from hyko_sdk.function import SDKFunction
from hyko_sdk.io import Audio
from hyko_sdk.metadata import CoreModel

func = SDKFunction(
    description="OpenAI Audio Transcription model (API).This model converts audio recordings into written text",
)


@func.set_input
class Inputs(CoreModel):
    audio: Audio = Field(..., description="Audio to be transcribed")


@func.set_param
class Params(CoreModel):
    prompt: Optional[str] = Field(
        default=None, description="User additional text prompt for the model"
    )
    language: Optional[str] = Field(
        default="en", description="ISO-639-1 transcription language"
    )
    api_key: str = Field(..., description="OpenAI API KEY")
    temperature: Optional[float] = Field(default=None, description="Model temperature")


@func.set_output
class Outputs(CoreModel):
    transcribed_text: str = Field(..., description="Generated transcription text")
