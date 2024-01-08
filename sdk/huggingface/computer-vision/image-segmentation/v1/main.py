"""
TODO handle the output of segmentation, now only one mask is supported and is
returned as a PIL image.
"""
import os

from fastapi import HTTPException
from pydantic import Field
from transformers import pipeline

from hyko_sdk.function import SDKFunction
from hyko_sdk.io import Image
from hyko_sdk.metadata import CoreModel

func = SDKFunction(
    description="HuggingFace image segmentation",
    requires_gpu=False,
)


class Inputs(CoreModel):
    input_image: Image = Field(..., description="Input image")


class Params(CoreModel):
    hugging_face_model: str = Field(
        ..., description="Model"
    )  # WARNING: DO NOT REMOVE! implementation specific
    device_map: str = Field(
        ..., description="Device map (Auto, CPU or GPU)"
    )  # WARNING: DO NOT REMOVE! implementation specific


class Outputs(CoreModel):
    mask: Image = Field(..., description="Segmented image")


segmenter = None


@func.on_startup
async def load():
    global segmenter

    if segmenter is not None:
        print("Model already Loaded")
        return

    model = os.getenv("HYKO_HF_MODEL")

    if model is None:
        raise HTTPException(status_code=500, detail="Model env not set")

    device_map = os.getenv("HYKO_DEVICE_MAP", "auto")

    segmenter = pipeline(
        "image-segmentation",
        model=model,
        device_map=device_map,
    )


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    if segmenter is None:
        raise HTTPException(status_code=500, detail="Model is not loaded yet")

    res = segmenter(inputs.input_image.to_pil())
    mask = Image.from_pil(res[0]["mask"])

    return Outputs(mask=mask)  # type: ignore
