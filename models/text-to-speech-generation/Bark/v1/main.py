from bark import SAMPLE_RATE, generate_audio, preload_models
from metadata import Inputs, Outputs, Params, func

from hyko_sdk.io import Audio


@func.on_startup
async def load():
    preload_models()  # grabs best device


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    audio_array = generate_audio(
        inputs.text,
        history_prompt=params.history,
        text_temp=params.text_tempreture,
        waveform_temp=params.waveform_temp,
    )
    audio = Audio.from_ndarray(arr=audio_array, sampling_rate=SAMPLE_RATE)

    return Outputs(audio=audio)
