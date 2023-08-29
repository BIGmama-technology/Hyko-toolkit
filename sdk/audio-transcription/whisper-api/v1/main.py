from fastapi import HTTPException, status
from hyko_sdk import CoreModel, SDKFunction, Audio
import openai
import io
from typing import Optional
from pydantic import Field


func = SDKFunction(
    description="OpenAI Audio Transcription model (API)",
    requires_gpu=False,
)

class Inputs(CoreModel):
    audio: Audio = Field(..., description="Audio to be transcribed")

class Params(CoreModel):
    prompt: Optional[str] = Field(default=None, description="User additional text prompt for the model")
    language: Optional[str] = Field(default='en', description="ISO-639-1 transcription language")
    api_key: str = Field(..., description="OpenAI API KEY")
    temperature: Optional[float] = Field(default=None, description="Model temperature")

class Outputs(CoreModel):
    transcribed_text: str = Field(..., description="Generated transcription text")

@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    
    file = io.BytesIO(inputs.audio.data)
    file.name = inputs.audio.get_name()

    res = await openai.Audio.atranscribe(
        model="whisper-1",
        file=file,
        api_key=params.api_key,
        prompt=params.prompt,
        language=params.language,
        temperature=params.temperature,
    )

    transcription = res.get("text") # type: ignore

    if transcription is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unknown error occured {res}",
        )
    
    return Outputs(transcribed_text=transcription)
