"""
TODO change model output type to json
"""
from fastapi import HTTPException
from pydantic import Field
from hyko_sdk import CoreModel, SDKFunction, Image
import os
from transformers import pipeline

func = SDKFunction(
    description="HuggingFace depth estimation",
    requires_gpu=False,
)


class Inputs(CoreModel):
    input_image: Image = Field(..., description="Input image")


class Params(CoreModel):
    hugging_face_model: str = Field(
        ..., description="Model"
    )  # WARNING: DO NOT REMOVE! implementation specific


class Outputs(CoreModel):
    summary: str = Field(..., description="Summary of objects detected")


detector = None


@func.on_startup
async def load():
    global detector

    if detector is not None:
        print("Model already Loaded")
        return

    model = os.getenv("HYKO_HF_MODEL")

    if model is None:
        raise HTTPException(status_code=500, detail="Model env not set")

    try:
        detector = pipeline("object-detection", model=model, device_map="cpu")

    except Exception as exc:
        import logging

        logging.error(exc)


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    if detector is None:
        raise HTTPException(status_code=500, detail="Model is not loaded yet")

    res = detector(inputs.input_image.to_pil())
    if len(res) == 0:
        summary = "No objects detected"
    else:
        summary = str(res)

    return Outputs(summary=summary)  # type: ignore
