import os

import transformers
from fastapi import HTTPException
from metadata import Inputs, Outputs, Params, func

translator = None


@func.on_startup
async def load():
    global translator

    if translator is not None:
        print("Model already Loaded")
        return

    model = os.getenv("HYKO_HF_MODEL")

    if model is None:
        raise HTTPException(status_code=500, detail="Model env not set")

    device_map = os.getenv("HYKO_DEVICE_MAP", "auto")

    translator = transformers.pipeline(
        task="translation",
        model=model,
        device_map=device_map,
    )


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    if translator is None:
        raise HTTPException(status_code=500, detail="Model is not loaded yet")

    res = translator(inputs.original_text)

    return Outputs(translation_text=res[0]["translation_text"])  # type: ignore
