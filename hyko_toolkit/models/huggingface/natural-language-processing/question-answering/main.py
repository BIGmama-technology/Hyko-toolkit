import os

import transformers
from fastapi import HTTPException
from metadata import Inputs, Outputs, Params, func

qa_model = None


@func.on_startup
async def load():
    global qa_model

    model = os.getenv("HYKO_HF_MODEL")

    if model is None:
        raise HTTPException(status_code=500, detail="Model env not set")

    device_map = os.getenv("HYKO_DEVICE_MAP", "auto")

    qa_model = transformers.pipeline(
        task="question-answering",
        model=model,
        device_map=device_map,
    )


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    if qa_model is None:
        raise HTTPException(status_code=500, detail="Model is not loaded yet")

    res = qa_model(question=inputs.question, context=inputs.context)  # type: ignore

    return Outputs(
        answer=res["answer"],  # type: ignore
        start=res["start"],  # type: ignore
        end=res["end"],  # type: ignore
        score=res["score"],  # type: ignore
    )
