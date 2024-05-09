from enum import Enum

import httpx
from hyko_sdk.components.components import Ext
from hyko_sdk.io import Audio
from hyko_sdk.models import CoreModel, Method
from pydantic import Field

from hyko_toolkit.exceptions import APICallError
from hyko_toolkit.registry import ToolkitAPI

func = ToolkitAPI(
    name="elevenlabs_speech_to_speech",
    task="elevenlabs",
    description="Use elevenlabs api for speech to speech.",
)


class VoiceIds(str, Enum):
    Adam = "pNInz6obpgDQGcFmaJgB"
    Dorothy = "ThT5KcBeYPX3keUQqHPh"
    Clyde = "2EiwWnXFnvU5JabPnv8n"
    Charlie = "IKne3meq5aSn9XLyUdCD"
    Freya = "jsCqWAovK2LkecY7zXl4"
    Gigi = "jBpfuIE2acCO8z3wKNLl"
    Harry = "SOYHLrjzK2X1ezoPC6cr"
    James = "ZQe5CZNOzWyzPSCn5a3c"


@func.set_input
class Inputs(CoreModel):
    audio_input: Audio = Field(..., description="The original audio to convert.")


@func.set_param
class Params(CoreModel):
    api_key: str = Field(description="API key")
    voice_id: VoiceIds = Field(
        default=VoiceIds.Harry,
        description="Voice id to convert to.",
    )


@func.set_output
class Outputs(CoreModel):
    output_audio: Audio = Field(..., description="Generated Audio.")


class Voice(CoreModel):
    voice: bytes


@func.on_call
async def call(inputs: Inputs, params: Params):
    async with httpx.AsyncClient() as client:
        res = await client.request(
            method=Method.post,
            url=f"https://api.elevenlabs.io/v1/speech-to-speech/{params.voice_id.value}",
            headers={
                "Accept": "application/json",
                "xi-api-key": params.api_key,
            },
            files={
                "audio": await inputs.audio_input.get_data(),
            },
            json={
                "model_id": "eleven_english_sts_v2",
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.8,
                    "style": 0.0,
                    "use_speaker_boost": True,
                },
            },
            timeout=60 * 5,
        )
    if res.is_success:
        response = Voice(voice=res.content)
    else:
        raise APICallError(status=res.status_code, detail=res.text)

    return Outputs(
        output_audio=await Audio(obj_ext=Ext.MP3).init_from_val(val=response.voice)
    )
