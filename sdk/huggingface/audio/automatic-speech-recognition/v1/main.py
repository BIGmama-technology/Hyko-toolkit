from fastapi import HTTPException
from pydantic import Field
from hyko_sdk import CoreModel, SDKFunction, Audio
import os
import numpy as np
from transformers import pipeline

func = SDKFunction(
    description="HuggingFace automatic speech recognition",
    requires_gpu=False,
)


class Inputs(CoreModel):
    speech: Audio = Field(..., description="Input speech")


class Params(CoreModel):
    hugging_face_model: str = Field(
        ..., description="Model"
    )  # WARNING: DO NOT REMOVE! implementation specific
    device_map: str = Field(
        ..., description="Device map (Auto, CPU or GPU)"
    )  # WARNING: DO NOT REMOVE! implementation specific


class Outputs(CoreModel):
    text: str = Field(..., description="Recognized speech text")


recognizer = None


@func.on_startup
async def load():
    global recognizer

    if recognizer is not None:
        print("Model already Loaded")
        return

    model = os.getenv("HYKO_HF_MODEL")

    if model is None:
        raise HTTPException(status_code=500, detail="Model env not set")

    device_map = os.getenv("HYKO_DEVICE_MAP", "auto")

    recognizer = pipeline(
        "automatic-speech-recognition",
        model=model,
        device_map=device_map,
    )


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    if recognizer is None:
        raise HTTPException(status_code=500, detail="Model is not loaded yet")

    audio_array, sample_rate = inputs.speech.to_ndarray()
    # divide audio array to 30s chunks and recognize each chunk
    segment_duration = 30  # ms
    segment_length = segment_duration * sample_rate
    num_chunks = len(audio_array) // segment_length
    chunks = np.array_split(audio_array, num_chunks)

    result = ""
    for c in chunks:
        result += recognizer({"sampling_rate": sample_rate, "raw": c})["text"]  # type: ignore

    return Outputs(text=result)  # type: ignore
