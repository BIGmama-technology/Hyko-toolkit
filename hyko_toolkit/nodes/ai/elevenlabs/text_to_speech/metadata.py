from enum import Enum

import httpx
from hyko_sdk.components.components import Ext, TextField
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.io import Audio
from hyko_sdk.models import CoreModel, Method
from hyko_sdk.utils import field

from hyko_toolkit.exceptions import APICallError

func = ToolkitNode(
    name="Elevenlabs text to speech",
    description="Use elevenlabs api to turn text into lifelike spoken audio.",
    cost=100,
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
    text: str = field(
        description="Text to convert to speech.",
        component=TextField(placeholder="Enter your text here", multiline=True),
    )


@func.set_param
class Params(CoreModel):
    api_key: str = field(
        description="API key", component=TextField(placeholder="API KEY", secret=True)
    )
    voice_id: VoiceIds = field(
        default=VoiceIds.Adam,
        description="Voice id to use.",
    )


@func.set_output
class Outputs(CoreModel):
    voice: Audio = field(description="Generated Audio.")


class Voice(CoreModel):
    voice: bytes


@func.on_call
async def call(inputs: Inputs, params: Params):
    async with httpx.AsyncClient() as client:
        res = await client.request(
            method=Method.post,
            url=f"https://api.elevenlabs.io/v1/text-to-speech/{params.voice_id.value}",
            headers={
                "Accept": "application/json",
                "xi-api-key": params.api_key,
            },
            json={
                "text": inputs.text,
                "model_id": "eleven_multilingual_v2",
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

    return Outputs(voice=await Audio(obj_ext=Ext.MP3).init_from_val(val=response.voice))
