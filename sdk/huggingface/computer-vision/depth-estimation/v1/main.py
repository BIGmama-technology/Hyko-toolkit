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
    depth_map: Image = Field(..., description="Output depth map")


estimator = None


@func.on_startup
async def load():
    global estimator

    if estimator is not None:
        print("Model already Loaded")
        return

    model = os.getenv("HYKO_HF_MODEL")

    if model is None:
        raise HTTPException(status_code=500, detail="Model env not set")

    try:
        estimator = pipeline("depth-estimation", model=model, device_map="cpu")

    except Exception as exc:
        import logging

        logging.error(exc)


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    if estimator is None:
        raise HTTPException(status_code=500, detail="Model is not loaded yet")

    res = estimator(inputs.input_image.to_pil())
    depth_map = Image.from_pil(res["depth"])

    return Outputs(depth_map=depth_map)  # type: ignore
