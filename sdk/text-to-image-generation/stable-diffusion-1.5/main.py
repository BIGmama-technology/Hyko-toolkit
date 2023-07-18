import fastapi
from fastapi.exceptions import HTTPException
from config import Inputs, Params, Outputs, Image
from diffusers import StableDiffusionPipeline
import torch
import numpy as np

app = fastapi.FastAPI()

model_pipeline = None
device = torch.device("cuda:1") if torch.cuda.is_available() else torch.device('cpu')

@app.post(
    "/load",
    response_model=None
)
def load():
    global model_pipeline
    if model_pipeline is not None:
        print("Model loaded already")
        return
    
    repo_id = "runwayml/stable-diffusion-v1-5"
    model_pipeline = StableDiffusionPipeline.from_pretrained(repo_id, torch_dtype = torch.float16)
    model_pipeline = model_pipeline.to(device)


@app.post(
    "/",
    response_model=Outputs
)
async def main(inputs: Inputs, params: Params):
    if model_pipeline is None:
        raise HTTPException(status_code=500, detail="Model is not loaded yet")
    
    prompt = inputs.input_prompt
    images = model_pipeline(prompt).images #type: ignore
    output_image_arr = np.asarray(images[0])
    print(output_image_arr.shape)
    img = Image.from_ndarray(output_image_arr)
    await img.wait_data()
    print(len(img.data), img.data[:100])
    return Outputs(generated_image = img)