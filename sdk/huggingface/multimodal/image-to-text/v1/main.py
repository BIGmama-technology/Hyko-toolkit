import os

from fastapi import HTTPException
from pydantic import Field
from transformers import pipeline

from hyko_sdk.function import SDKFunction
from hyko_sdk.io import Image
from hyko_sdk.metadata import CoreModel

func = SDKFunction(
    description="Hugging Face Image-To-Text Task",
    requires_gpu=False,
)


class Inputs(CoreModel):
    image: Image = Field(..., description="Input image")


class Params(CoreModel):
    hugging_face_model: str = Field(
        ..., description="Model"
    )  # WARNING: DO NOT REMOVE! implementation specific
    device_map: str = Field(
        ..., description="Device map (Auto, CPU or GPU)"
    )  # WARNING: DO NOT REMOVE! implementation specific


class Outputs(CoreModel):
    generated_text: str = Field(..., description="Generated text")


captioner = None


@func.on_startup
async def load():
    global captioner

    if captioner is not None:
        print("Model already Loaded")
        return

    model = os.getenv("HYKO_HF_MODEL")

    if model is None:
        raise HTTPException(status_code=500, detail="Model env not set")

    device_map = os.getenv("HYKO_DEVICE_MAP", "auto")

    captioner = pipeline(
        task="image-to-text",
        model=model,
        device_map=device_map,
    )


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    if captioner is None:
        raise HTTPException(status_code=500, detail="Model is not loaded yet")

    res = captioner(inputs.image.to_pil())

    return Outputs(generated_text=res[0]["generated_text"])  # type: ignore
