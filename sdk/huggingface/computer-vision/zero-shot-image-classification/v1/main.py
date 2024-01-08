import os

from fastapi import HTTPException
from pydantic import Field
from transformers import pipeline

from hyko_sdk.function import SDKFunction
from hyko_sdk.io import Image
from hyko_sdk.metadata import CoreModel

func = SDKFunction(
    description="Hugging Face image classification",
    requires_gpu=False,
)


class Inputs(CoreModel):
    input_image: Image = Field(..., description="Input image")
    labels: list[str] = Field(..., description="Labels for classification")


class Params(CoreModel):
    hugging_face_model: str = Field(
        ..., description="Model"
    )  # WARNING: DO NOT REMOVE! implementation specific
    device_map: str = Field(
        ..., description="Device map (Auto, CPU or GPU)"
    )  # WARNING: DO NOT REMOVE! implementation specific


class Outputs(CoreModel):
    summary: str = Field(..., description="Summary of the classification")


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

    classifier = pipeline(
        "zero-shot-image-classification",
        model=model,
        device_map=device_map,
    )


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    if classifier is None:
        raise HTTPException(status_code=500, detail="Model is not loaded yet")

    res = classifier(inputs.input_image.to_pil(), candidate_labels=inputs.labels)

    return Outputs(summary=str(res))  # type: ignore
