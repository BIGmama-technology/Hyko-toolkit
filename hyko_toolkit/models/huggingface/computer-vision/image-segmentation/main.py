"""
TODO handle the output of segmentation, now only one mask is supported and is
returned as a PIL image.
"""
import os

from fastapi import HTTPException
from metadata import Inputs, Outputs, Params, func
from transformers import pipeline

from hyko_sdk.io import Image

segmenter = None


@func.on_startup
async def load():
    global segmenter

    model = os.getenv("HYKO_HF_MODEL")

    if model is None:
        raise HTTPException(status_code=500, detail="Model env not set")

    device_map = os.getenv("HYKO_DEVICE_MAP", "auto")

    segmenter = pipeline(
        "image-segmentation",
        model=model,
        device_map=device_map,
    )


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    if segmenter is None:
        raise HTTPException(status_code=500, detail="Model is not loaded yet")

    res = segmenter(inputs.input_image.to_pil())
    mask = Image.from_pil(res[0]["mask"])

    return Outputs(mask=mask)
