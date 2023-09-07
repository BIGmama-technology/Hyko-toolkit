import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import torch
from fastapi import HTTPException
from transformers import BlipProcessor, BlipForConditionalGeneration # type: ignore
from pydantic import Field
from hyko_sdk import CoreModel, SDKFunction, Image



func = SDKFunction(
    description="An image captioning model, gives a short description of the input image",
    requires_gpu=False,
)

class Inputs(CoreModel):
    image : Image = Field(..., description="User input image to be captionned")


class Params(CoreModel):
    pass

class Outputs(CoreModel):
    image_description : str = Field(..., description="description caption of the image")

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


    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")


@func.on_execute
async def main(inputs: Inputs, params: Params)-> Outputs:
    if model is None or processor is None:
        raise HTTPException(status_code=500, detail="Model is not loaded yet")
    
    img = inputs.image.to_ndarray() # type: ignore
    inputs = processor(img, return_tensors="pt")

    with torch.no_grad():
         outputs = model.generate(**inputs)

    caption = processor.decode(outputs[0], skip_special_tokens=True)
   

    return Outputs(image_description=caption)
