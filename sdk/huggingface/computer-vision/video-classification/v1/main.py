from fastapi import HTTPException
from pydantic import Field
from hyko_sdk import CoreModel, SDKFunction, Video
import os
from transformers import pipeline

func = SDKFunction(
    description="HuggingFace video classification",
    requires_gpu=False,
)


class Inputs(CoreModel):
    input_video: Video = Field(..., description="Input image")


class Params(CoreModel):
    hugging_face_model: str = Field(
        ..., description="Model"
    )  # WARNING: DO NOT REMOVE! implementation specific
    device_map: str = Field(
        ..., description="Device map (Auto, CPU or GPU)"
    )  # WARNING: DO NOT REMOVE! implementation specific


class Outputs(CoreModel):
    summary: str = Field(..., description="Summary of results")


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
        "video-classification",
        model=model,
        device_map=device_map,
    )


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    if segmenter is None:
        raise HTTPException(status_code=500, detail="Model is not loaded yet")

    _, ext = os.path.splitext(inputs.input_video.get_name())

    with open(f"/app/video.{ext}", "wb") as f:
        f.write(inputs.input_video.get_data())

    res = segmenter(f"/app/video.{ext}")

    return Outputs(summary=str(res))  # type: ignore
