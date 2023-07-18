from config import Inputs, Outputs, Params
from transformers import AutoImageProcessor, SegformerModel
import torch
import base64
import numpy as np
import cv2
import fastapi
from hyko_sdk.io import image_to_base64
from fastapi import HTTPException
app = fastapi.FastAPI()
model = None
image_processor = None
device = torch.device("cuda") if torch.cuda.is_available() else torch.device('cpu')
@app.post("/load", response_model=None)
def load():
    global model
    global image_processor
    if model is not None and image_processor is not None:
        print("Model loaded already")
        return

    image_processor = AutoImageProcessor.from_pretrained("nvidia/mit-b0")
    model = SegformerModel.from_pretrained("nvidia/mit-b0").cuda()

@app.post("/", response_model=Outputs)
async def main(inputs: Inputs, params: Params):
    if model is None or image_processor is None:
        raise HTTPException(status_code=500, detail="Model is not loaded yet")
    
    img = image_processor(inputs.img.decode())
    # print(" ------------",torch.FloatTensor(inputs.pixel_values[0]).shape)
    with torch.no_grad():
        outputs = model(torch.FloatTensor(img.pixel_values[0])[None,:].cuda())

    # print(outputs.last_hidden_state)
    array = outputs.last_hidden_state.cpu().numpy()
    # print(array.squeeze()[:3].shape)
    array = np.swapaxes(array.squeeze()[0:3], 0 ,-1)
    array = array / array.max()
    array = 255 * array
    array = array.astype(np.uint8)
    print("---->", array.shape)
    # print(image[1].shape)
   
    return Outputs(img=image_to_base64(array))