from typing import Optional
from pydantic import Field
from hyko_sdk import CoreModel, Audio, extract_metadata

description = "OpenAI's Audio Transcription model (API)"

class Inputs(CoreModel):
    audio: Audio = Field(..., description="User audio input to be transcribed")

class Params(CoreModel):
    prompt: Optional[str] = Field(default=None, description="User additional text prompt for the model")
    language: Optional[str] = Field(default='en', description="ISO-639-1 transcription language")
    api_key: str = Field(..., description="OpenAI's API KEY")
    temperature: Optional[float] = Field(default=None, description="Whisper model temperature")

class Outputs(CoreModel):
    transcribed_text: str = Field(..., description="Generated transcription text")


if __name__ == "__main__":
    extract_metadata(
                    Inputs, Params, Outputs,  # type: ignore
                    description, False
                )
