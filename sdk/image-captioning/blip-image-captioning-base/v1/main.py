import numpy as np
import torch
from fastapi import HTTPException
from transformers import BlipProcessor, BlipForConditionalGeneration # type: ignore
import os
from PIL import Image as PIL_Image
from pydantic import Field
from hyko_sdk import CoreModel, SDKFunction, Image



func = SDKFunction(
    description="An image captioning model, gives a short description of the input image",
    requires_gpu=False,
)

class Inputs(CoreModel):
    image : Image = Field(..., description="User inputted image to be captionned")


class Params(CoreModel):
    pass

class Outputs(CoreModel):
    image_description : str = Field(..., description="description/caption of the image")

model = None
processor = None
tokenizer = None
device = torch.device("cuda") if torch.cuda.is_available() else torch.device('cpu')

@func.on_startup
async def load():
    global model
    global processor
    if model is not None and processor is not None:
        print("Model loaded already")
        return


    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")


@func.on_execute
async def main(inputs: Inputs, params: Params):
    if model is None or processor is None:
        raise HTTPException(status_code=500, detail="Model is not loaded yet")
    

    file, ext = os.path.splitext(inputs.image.get_name())
    with open(f"./image{ext}", "wb") as f:
        f.write(inputs.image.get_data())

    
    image = PIL_Image.open(f"./image{ext}")
    img = np.array(image)
    img = inputs.image.to_ndarray()
    inputs = processor(img, return_tensors="pt")

    with torch.no_grad():
         outputs = model.generate(**inputs)

    caption = processor.decode(outputs[0], skip_special_tokens=True)
   

    return Outputs(image_description=caption)