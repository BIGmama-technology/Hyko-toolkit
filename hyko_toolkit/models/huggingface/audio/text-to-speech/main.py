import os

from fastapi import HTTPException
from metadata import Inputs, Outputs, Params, func
from transformers import pipeline

from hyko_sdk.io import Audio

synthesizer = None


@func.on_startup
async def load():
    global synthesizer

    model = os.getenv("HYKO_HF_MODEL")
    device_map = os.getenv("HYKO_DEVICE_MAP", "auto")

    if model is None:
        raise HTTPException(status_code=500, detail="Model env not set")

    synthesizer = pipeline("text-to-speech", model=model, device_map=device_map)


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    if synthesizer is None:
        raise HTTPException(status_code=500, detail="Model is not loaded yet")

    result_audio = synthesizer(inputs.text)
    result_audio = Audio.from_ndarray(
        result_audio["audio"], sampling_rate=result_audio["sampling_rate"]
    )

    return Outputs(speech=result_audio)  # type: ignore
