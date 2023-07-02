import fastapi
from fastapi.exceptions import HTTPException
from config import Inputs, Params, Outputs
from diffusers import StableDiffusionPipeline
import torch
import base64
import numpy as np
import PIL

from hyko_sdk.io import image_to_base64

device : torch.device 

if torch.cuda.is_available():
    device = torch.device("cuda:0")
else:
    device = torch.device("cpu")

app = fastapi.FastAPI()
repo_id = "runwayml/stable-diffusion-v1-5"
model_pipeline = StableDiffusionPipeline.from_pretrained(repo_id, torch_dtype = torch.float16)
model_pipeline = model_pipeline.to(device)
#################################################################

@app.post("/", response_model=Outputs)
async def main(inputs: Inputs, params: Params):
    prompt = inputs.input_prompt
    images = model_pipeline(prompt).images
    output_image_arr = np.asarray(images[0])
    images[0].save("StableDiff-Test.png")
    return Outputs(generated_image = image_to_base64(output_image_arr))