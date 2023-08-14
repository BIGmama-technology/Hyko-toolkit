from config import Inputs, Outputs, Params, Image
from transformers import AutoImageProcessor, SegformerModel
import torch
import numpy as np
import fastapi
from fastapi import HTTPException

app = fastapi.FastAPI()

model = None
image_processor = None
device = torch.device("cuda") if torch.cuda.is_available() else torch.device('cpu')

@app.post(
    "/load",
    response_model=None
)
def load():
    global model
    global image_processor
    if model is not None and image_processor is not None:
        print("Model loaded already")
        return

    image_processor = AutoImageProcessor.from_pretrained("nvidia/mit-b0")
    model = SegformerModel.from_pretrained("nvidia/mit-b0").to(device) # type: ignore 

@app.post(
    "/", 
    response_model=Outputs
)
async def main(inputs: Inputs, params: Params):
    if model is None or image_processor is None:
        raise HTTPException(status_code=500, detail="Model is not loaded yet")
    
    await inputs.image.wait_data()
    img = inputs.image.to_ndarray()
    
    img = image_processor(img)
    with torch.no_grad():
        outputs = model(torch.FloatTensor(img.pixel_values[0])[None,:].cuda())

    array = outputs.last_hidden_state.cpu().numpy()
    array = np.swapaxes(array.squeeze()[0:3], 0 ,-1)
    array = array / array.max()
    array = 255 * array
    array = array.astype(np.uint8)
    segmented_image = Image.from_ndarray(array)
    await segmented_image.wait_data()
    return Outputs(segmented_image=segmented_image)