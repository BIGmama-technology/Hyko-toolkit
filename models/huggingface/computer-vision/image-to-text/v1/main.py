import os

from fastapi import HTTPException
from metadata import Inputs, Outputs, Params, func
from transformers import pipeline

captioner = None


@func.on_startup
async def load():
    global captioner

    if captioner is not None:
        print("Model already Loaded")
        return

    model = os.getenv("HYKO_HF_MODEL")

    if model is None:
        raise HTTPException(status_code=500, detail="Model env not set")

    device_map = os.getenv("HYKO_DEVICE_MAP", "auto")

    captioner = pipeline(
        "image-to-text",
        model=model,
        device_map=device_map,
    )


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    if captioner is None:
        raise HTTPException(status_code=500, detail="Model is not loaded yet")

    res = captioner(inputs.input_image.to_pil())

    return Outputs(caption=res[0]["generated_text"])  # type: ignore
