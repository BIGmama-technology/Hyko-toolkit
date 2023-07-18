import fastapi
from fastapi.exceptions import HTTPException
from config import Inputs, Params, Outputs
from diffusers import StableDiffusionPipeline
import torch
import base64
import numpy as np
import PIL

from hyko_sdk.io import image_to_base64

app = fastapi.FastAPI()

model_pipeline = None
device = torch.device("cuda:2") if torch.cuda.is_available() else torch.device('cpu')
@app.post("/load", response_model=None)
def load():
    global model_pipeline
    if model_pipeline is not None:
        print("Model loaded already")
        return
    
    repo_id = "runwayml/stable-diffusion-v1-5"
    model_pipeline = StableDiffusionPipeline.from_pretrained(repo_id, torch_dtype = torch.float16)
    model_pipeline = model_pipeline.to(device)

#################################################################

@app.post("/", response_model=Outputs)
async def main(inputs: Inputs, params: Params):
    if model_pipeline is None:
        raise HTTPException(status_code=500, detail="Model is not loaded yet")
    
    prompt = inputs.input_prompt
    images = model_pipeline(prompt).images
    output_image_arr = np.asarray(images[0])
    # images[0].save("StableDiff-Test.png")
    return Outputs(generated_image = image_to_base64(output_image_arr))