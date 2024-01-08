import os

from fastapi import HTTPException
from pydantic import Field
from transformers import pipeline

from hyko_sdk.function import SDKFunction
from hyko_sdk.io import Audio
from hyko_sdk.metadata import CoreModel

func = SDKFunction(
    description="HuggingFace text to speech, run on cude may cause issues on cpu",
    requires_gpu=False,
)


class Inputs(CoreModel):
    text: str = Field(..., description="Input text")


class Params(CoreModel):
    hugging_face_model: str = Field(
        ..., description="Model"
    )  # WARNING: DO NOT REMOVE! implementation specific
    device_map: str = Field(
        ..., description="Device map (Auto, CPU or GPU)"
    )  # WARNING: DO NOT REMOVE! implementation specific


class Outputs(CoreModel):
    speech: Audio = Field(..., description="Synthesized speech")


synthesizer = None


@func.on_startup
async def load():
    global synthesizer

    if synthesizer is not None:
        print("Model already Loaded")
        return

    model = os.getenv("HYKO_HF_MODEL")
    device_map = os.getenv("HYKO_DEVICE_MAP", "auto")

    if model is None:
        raise HTTPException(status_code=500, detail="Model env not set")

    try:
        synthesizer = pipeline("text-to-speech", model=model, device_map=device_map)

    except Exception as exc:
        import logging

        logging.error(exc)


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    if synthesizer is None:
        raise HTTPException(status_code=500, detail="Model is not loaded yet")

    result_audio = synthesizer(inputs.text)
    result_audio = Audio.from_ndarray(
        result_audio["audio"], sampling_rate=result_audio["sampling_rate"]
    )

    return Outputs(speech=result_audio)  # type: ignore
