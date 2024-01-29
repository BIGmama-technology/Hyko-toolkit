import os

from fastapi import HTTPException
from metadata import Inputs, Outputs, Params, func
from transformers import pipeline

classifier = None


@func.on_startup
async def load():
    global classifier

    model = os.getenv("HYKO_HF_MODEL")

    if model is None:
        raise HTTPException(status_code=500, detail="Model env not set")

    device_map = os.getenv("HYKO_DEVICE_MAP", "auto")

    classifier = pipeline(
        "zero-shot-image-classification",
        model=model,
        device_map=device_map,
    )


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    res = classifier(inputs.input_image.to_pil(), candidate_labels=inputs.labels)

    return Outputs(summary=str(res))  # type: ignore
