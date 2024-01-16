import os

from fastapi import HTTPException
from metadata import Inputs, Outputs, Params, func
from transformers import pipeline

segmenter = None


@func.on_startup
async def load():
    global segmenter

    if segmenter is not None:
        print("Model already Loaded")
        return

    model = os.getenv("HYKO_HF_MODEL")

    if model is None:
        raise HTTPException(status_code=500, detail="Model env not set")

    device_map = os.getenv("HYKO_DEVICE_MAP", "auto")

    segmenter = pipeline(
        "video-classification",
        model=model,
        device_map=device_map,
    )


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    if segmenter is None:
        raise HTTPException(status_code=500, detail="Model is not loaded yet")

    _, ext = os.path.splitext(inputs.input_video.get_name())

    with open(f"/app/video.{ext}", "wb") as f:
        f.write(inputs.input_video.get_data())

    res = segmenter(f"/app/video.{ext}")

    return Outputs(summary=str(res))  # type: ignore
