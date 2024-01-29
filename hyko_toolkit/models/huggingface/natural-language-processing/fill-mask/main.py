import os

import transformers
from fastapi import HTTPException
from metadata import Inputs, Outputs, Params, func

filler = None


@func.on_startup
async def load():
    global filler

    model = os.getenv("HYKO_HF_MODEL")

    if model is None:
        raise HTTPException(status_code=500, detail="Model env not set")

    device_map = os.getenv("HYKO_DEVICE_MAP", "auto")

    filler = transformers.pipeline(
        task="fill-mask",
        model=model,
        device_map=device_map,
    )


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    if filler is None:
        raise HTTPException(status_code=500, detail="Model is not loaded yet")

    res = filler(inputs.masked_text)

    return Outputs(sequence=res[0]["sequence"], score=res[0]["score"])  # type: ignore
