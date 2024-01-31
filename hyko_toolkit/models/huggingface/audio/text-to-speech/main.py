from metadata import Inputs, Outputs, Params, StartupParams, func
from transformers import pipeline

from hyko_sdk.io import Audio

synthesizer = None


@func.on_startup
async def load(startup_params: StartupParams):
    global synthesizer

    model = startup_params.hugging_face_model
    device_map = startup_params.device_map

    synthesizer = pipeline("text-to-speech", model=model, device_map=device_map)


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    result_audio = synthesizer(inputs.text)
    result_audio = Audio.from_ndarray(
        result_audio["audio"], sampling_rate=result_audio["sampling_rate"]
    )

    return Outputs(speech=result_audio)  # type: ignore
