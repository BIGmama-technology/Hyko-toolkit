import os

from fastapi import HTTPException
from metadata import Inputs, Outputs, Params, func
from transformers import pipeline

from hyko_sdk.io import Image

estimator = None


@func.on_startup
async def load():
    global estimator

    if estimator is not None:
        print("Model already Loaded")
        return

    model = os.getenv("HYKO_HF_MODEL")

    if model is None:
        raise HTTPException(status_code=500, detail="Model env not set")

    device_map = os.getenv("HYKO_DEVICE_MAP", "auto")

    estimator = pipeline(
        "depth-estimation",
        model=model,
        device_map=device_map,
    )


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    if estimator is None:
        raise HTTPException(status_code=500, detail="Model is not loaded yet")

    res = estimator(inputs.input_image.to_pil())
    depth_map = Image.from_pil(res["depth"])

    return Outputs(depth_map=depth_map)  # type: ignore
