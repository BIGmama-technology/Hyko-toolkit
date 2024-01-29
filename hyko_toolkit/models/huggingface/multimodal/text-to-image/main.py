import os

from diffusers.pipelines.pipeline_utils import DiffusionPipeline
from fastapi import HTTPException
from metadata import Inputs, Outputs, Params, func

from hyko_sdk.io import Image

generator = None


@func.on_startup
async def load():
    global generator

    model = os.getenv("HYKO_HF_MODEL")

    if model is None:
        raise HTTPException(status_code=500, detail="Model env not set")

    device_map = os.getenv("HYKO_DEVICE_MAP")

    if device_map == "auto":
        raise RuntimeError("device_map should not be auto")

    generator = DiffusionPipeline.from_pretrained(
        pretrained_model_name_or_path=model,
    )

    if device_map.startswith("cuda"):
        generator.to(device_map)


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    res = generator(inputs.prompt)

    return Outputs(generated_image=Image.from_pil(res.images[0]))  # type: ignore
