import os

from fastapi import HTTPException
from metadata import Inputs, Outputs, Params, func
from transformers import pipeline

detector = None


@func.on_startup
async def load():
    global detector

    model = os.getenv("HYKO_HF_MODEL")

    if model is None:
        raise HTTPException(status_code=500, detail="Model env not set")

    device_map = os.getenv("HYKO_DEVICE_MAP", "auto")

    detector = pipeline(
        "object-detection",
        model=model,
        device_map=device_map,
    )


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    if detector is None:
        raise HTTPException(status_code=500, detail="Model is not loaded yet")

    res = detector(inputs.input_image.to_pil())
    if len(res) == 0:
        summary = "No objects detected"
    else:
        summary = str(res)

    return Outputs(summary=summary)  # type: ignore
