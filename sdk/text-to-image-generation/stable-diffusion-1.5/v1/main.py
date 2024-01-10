import os

import numpy as np
import torch
from diffusers import StableDiffusionPipeline
from fastapi.exceptions import HTTPException
from metadata import Inputs, Outputs, Params, func

from hyko_sdk.io import Image

model_pipeline = None


@func.on_startup
async def load():
    global model_pipeline
    if model_pipeline is not None:
        print("Model loaded already")
        return

    device = os.getenv("HYKO_DEVICE_MAP", "cuda")
    model_pipeline = StableDiffusionPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5", torch_dtype=torch.float16
    )
    model_pipeline = model_pipeline.to(device)


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    if model_pipeline is None:
        raise HTTPException(status_code=500, detail="Model is not loaded yet")

    prompt = inputs.prompt
    images = model_pipeline(prompt).images  # type: ignore
    output_image_arr = np.asarray(images[0])
    print(output_image_arr.shape)
    img = Image.from_ndarray(output_image_arr)
    print(len(img.get_data()), img.get_data()[:100])
    return Outputs(generated_image=img)
