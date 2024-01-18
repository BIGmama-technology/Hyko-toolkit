import os

import transformers
from fastapi import HTTPException
from metadata import Inputs, Outputs, Params, func

classifier = None


@func.on_startup
async def load():
    global classifier

    if classifier is not None:
        print("Model already Loaded")
        return

    model = os.getenv("HYKO_HF_MODEL")

    if model is None:
        raise HTTPException(status_code=500, detail="Model env not set")

    device_map = os.getenv("HYKO_DEVICE_MAP", "auto")

    classifier = transformers.pipeline(
        task="text-classification",
        model=model,
        device_map=device_map,
    )


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    if classifier is None:
        raise HTTPException(status_code=500, detail="Model is not loaded yet")

    res = classifier(inputs.input_text)

    return Outputs(label=res[0]["label"], score=res[0]["score"])  # type: ignore
