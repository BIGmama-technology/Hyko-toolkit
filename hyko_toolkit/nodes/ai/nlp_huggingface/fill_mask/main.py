import transformers
from fastapi import HTTPException

from .metadata import Inputs, Outputs, Params, node


@node.on_startup
async def load(startup_params: Params):
    global filler

    model = startup_params.hugging_face_model
    device_map = startup_params.device_map

    filler = transformers.pipeline(
        model=model,
        device_map=device_map,
    )


@node.on_call
async def main(inputs: Inputs, params: Params) -> Outputs:
    if filler is None:
        raise HTTPException(status_code=500, detail="Model is not loaded yet")

    res = filler(inputs.masked_text, top_k=params.top_k)
    sequences = [prediction["sequence"] for prediction in res]
    scores = [prediction["score"] for prediction in res]
    return Outputs(sequence=sequences, score=scores)  # type: ignore
