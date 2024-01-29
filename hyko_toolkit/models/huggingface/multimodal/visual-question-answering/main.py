import os

from fastapi import HTTPException
from metadata import Inputs, Outputs, Params, func
from transformers import pipeline

vqa_pipeline = None


@func.on_startup
async def load():
    global vqa_pipeline

    model = os.getenv("HYKO_HF_MODEL")

    if model is None:
        raise HTTPException(status_code=500, detail="Model env not set")

    device_map = os.getenv("HYKO_DEVICE_MAP", "auto")

    vqa_pipeline = pipeline(
        task="visual-question-answering",
        model=model,
        device_map=device_map,
    )


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    if vqa_pipeline is None:
        raise HTTPException(status_code=500, detail="Model is not loaded yet")

    res = vqa_pipeline(
        image=inputs.image.to_pil(), question=inputs.question, top_k=params.top_k
    )

    return Outputs(answer=res[0]["answer"], score=res[0]["score"])  # type: ignore
