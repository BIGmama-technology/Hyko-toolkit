from fastapi.exceptions import HTTPException
from diffusers import StableDiffusionPipeline
import torch
import numpy as np
from pydantic import Field
from hyko_sdk import CoreModel, SDKFunction, Image


func = SDKFunction(
    description="Text to Image Generation Model",
    requires_gpu=True,
)

class Inputs(CoreModel):
    prompt: str = Field(..., description="User text prompt")

class Params(CoreModel):
    pass

class Outputs(CoreModel):
    generated_image: Image = Field(..., description="AI Generated image described by user text prompt")


model_pipeline = None
device = torch.device("cuda:1") if torch.cuda.is_available() else torch.device('cpu')

@func.on_startup
async def load():
    global model_pipeline
    if model_pipeline is not None:
        print("Model loaded already")
        return
    
    repo_id = "runwayml/stable-diffusion-v1-5"
    model_pipeline = StableDiffusionPipeline.from_pretrained(repo_id, torch_dtype = torch.float16)
    model_pipeline = model_pipeline.to(device)


@func.on_execute
async def main(inputs: Inputs, params: Params)-> Outputs:
    if model_pipeline is None:
        raise HTTPException(status_code=500, detail="Model is not loaded yet")
    
    prompt = inputs.prompt
    images = model_pipeline(prompt).images      #type: ignore
    output_image_arr = np.asarray(images[0])
    print(output_image_arr.shape)
    img = Image.from_ndarray(output_image_arr)
    print(len(img.get_data()), img.get_data()[:100])
    return Outputs(generated_image = img)