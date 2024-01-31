import numpy as np
from fastapi import HTTPException
from metadata import Inputs, Outputs, Params, StartupParams, func
from transformers import pipeline

recognizer = None


@func.on_startup
async def load(startup_params: StartupParams):
    global recognizer

    model = startup_params.hugging_face_model
    device_map = startup_params.device_map

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
