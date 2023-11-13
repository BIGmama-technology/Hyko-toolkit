from fastapi import HTTPException
from pydantic import Field
from hyko_sdk import CoreModel, SDKFunction
import transformers
import os

func = SDKFunction(
    description="Hugging Face fill mask task",
    requires_gpu=False,
)


class Inputs(CoreModel):
    masked_text: str = Field(..., description="Input text with <mask> to fill")


class Params(CoreModel):
    hugging_face_model: str = Field(
        ..., description="Model"
    )  # WARNING: DO NOT REMOVE! implementation specific
    device_map: str = Field(
        ..., description="Device map (Auto, CPU or GPU)"
    )  # WARNING: DO NOT REMOVE! implementation specific


class Outputs(CoreModel):
    sequence: str = Field(..., description="Filled output text")
    score: float = Field(..., description="Score of the filled sequence")


filler = None


@func.on_startup
async def load():
    global filler

    if filler is not None:
        print("Model already Loaded")
        return

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
