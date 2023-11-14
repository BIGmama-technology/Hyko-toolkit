from fastapi import HTTPException
from pydantic import Field
from hyko_sdk import CoreModel, SDKFunction, Image
from diffusers.pipelines.pipeline_utils import DiffusionPipeline
import os


func = SDKFunction(
    description="Hugging Face Text to Image Task",
    requires_gpu=False,
)


class Inputs(CoreModel):
    prompt: str = Field(..., description="Input text")

class Params(CoreModel):
    hugging_face_model: str = Field(
        ..., description="Model"
    )  # WARNING: DO NOT REMOVE! implementation specific
    device_map: str = Field(
        ..., description="Device map (Auto, CPU or GPU)"
    )  # WARNING: DO NOT REMOVE! implementation specific

class Outputs(CoreModel):
    generated_image: Image = Field(..., description="Generated image")


generator = None


@func.on_startup
async def load():
    global generator

    if generator is not None:
        print("Model already Loaded")
        return

    model = os.getenv("HYKO_HF_MODEL")

    if model is None:
        raise HTTPException(status_code=500, detail="Model env not set")

    device_map = os.getenv("HYKO_DEVICE_MAP", "auto")

    generator = DiffusionPipeline.from_pretrained(
        pretrained_model_name_or_path=model,
        device_map=device_map,
    )


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    if generator is None:
        raise HTTPException(status_code=500, detail="Model is not loaded yet")

    res = generator(inputs.prompt)

    return Outputs(generated_image=Image.from_pil(res.images[0]))  # type: ignore
