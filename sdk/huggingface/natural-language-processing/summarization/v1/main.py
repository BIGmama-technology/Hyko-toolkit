import os

import transformers
from fastapi import HTTPException
from pydantic import Field

from hyko_sdk.function import SDKFunction
from hyko_sdk.metadata import CoreModel

func = SDKFunction(
    description="Hugging Face summarization",
    requires_gpu=False,
)


class Inputs(CoreModel):
    input_text: str = Field(..., description="text to summarize")


class Params(CoreModel):
    hugging_face_model: str = Field(
        ..., description="Model"
    )  # WARNING: DO NOT REMOVE! implementation specific
    device_map: str = Field(
        ..., description="Device map (Auto, CPU or GPU)"
    )  # WARNING: DO NOT REMOVE! implementation specific
    min_length: int = Field(default=30, description="Minimum output length")
    max_length: int = Field(default=130, description="Maximum output length")


class Outputs(CoreModel):
    summary_text: str = Field(..., description="Summary output")


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
        task="summarization",
        model=model,
        device_map=device_map,
    )


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    if classifier is None:
        raise HTTPException(status_code=500, detail="Model is not loaded yet")

    res = classifier(
        inputs.input_text, min_length=params.min_length, max_length=params.max_length
    )

    return Outputs(summary_text=res[0]["summary_text"])  # type: ignore
