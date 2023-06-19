from .config import Inputs, Outputs, Params
from transformers import AutoImageProcessor, SegformerModel
import torch
import base64
import numpy as np
import cv2
import fastapi

app = fastapi.FastAPI()

image_processor = AutoImageProcessor.from_pretrained("nvidia/mit-b0")
model = SegformerModel.from_pretrained("nvidia/mit-b0").cuda()

@app.post("/", response_model=Outputs)
async def main(inputs: Inputs, params: Params):
    i_image = base64.urlsafe_b64decode(inputs.img)
    npimg = np.frombuffer(i_image, np.uint8)
    print("->", npimg.shape)
    cvimg = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    # print(cvimg.shape)
    inputs = image_processor(cv2.cvtColor(cvimg, cv2.COLOR_BGR2RGB))
    # print(" ------------",torch.FloatTensor(inputs.pixel_values[0]).shape)
    with torch.no_grad():
        outputs = model(torch.FloatTensor(inputs.pixel_values[0])[None,:].cuda())

    # print(outputs.last_hidden_state)
    array = outputs.last_hidden_state.cpu().numpy()
    # print(array.squeeze()[:3].shape)
    array = np.swapaxes(array.squeeze()[0:3], 0 ,-1)
    array = array / array.max()
    array = 255 * array
    array = array.astype(np.uint8)
    print("---->", array.shape)
    # print(image[1].shape)
    cv2.imwrite("segment_test.png", array)
    image = cv2.imencode(array, cv2.IMREAD_COLOR)
    
    segments = base64.urlsafe_b64encode(array.reshape(-1)) # HERE
    # segments = array.tobytes()
    print(segments)
    return Outputs(img=segments)