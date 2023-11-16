from pydantic import Field
from hyko_sdk import CoreModel, SDKFunction, Audio
from bark import SAMPLE_RATE, generate_audio, preload_models

func = SDKFunction(

    description="Generate audio from a given prompt",
    requires_gpu=False,
)

class Inputs(CoreModel):
    text : str = Field(..., description="Prompt for audio generation")


class Params(CoreModel):
    history_prompt : str = Field(default="", description="History prompts for audio generation")
    text_tempreture : float = Field(default=0.5, description="Generation temperature (1.0 more diverse, 0.0 more conservative)")
    waveform_temp : float = Field(default=0.5, description="generation temperature (1.0 more diverse, 0.0 more conservative")

class Outputs(CoreModel):
    audio : Audio = Field(..., description="Generated audio")


@func.on_startup
async def load():
    preload_models() # grabs best device

@func.on_execute
async def main(inputs: Inputs, params: Params)-> Outputs:
    audio_array = generate_audio(inputs.text, history_prompt=params.history_prompt, text_temp=params.text_tempreture, waveform_temp=params.waveform_temp)
    audio = Audio.from_ndarray(arr=audio_array, sampling_rate=SAMPLE_RATE)
 
    return Outputs(audio=audio)