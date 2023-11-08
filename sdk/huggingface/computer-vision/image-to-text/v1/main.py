from fastapi import HTTPException
from pydantic import Field
from hyko_sdk import CoreModel, SDKFunction, Image
import os
from transformers import pipeline

func = SDKFunction(
    description="Hugging Face image captioning",
    requires_gpu=False,
)

class Inputs(CoreModel):
    input_image: Image = Field(..., description="Input image")

class Params(CoreModel):
    hugging_face_model: str = Field(..., description="Model") # WARNING: DO NOT REMOVE! implementation specific

class Outputs(CoreModel):
    caption: str = Field(..., description="Image caption")


captioner = None

@func.on_startup
async def load():
    global captioner
    
    if captioner is not None:
        print("Model already Loaded")
        return
    
    model = os.getenv("HYKO_HF_MODEL")
    
    if model is None:
        raise HTTPException(status_code=500, detail="Model env not set")
    
    try:
        captioner = pipeline(
        "image-to-text", 
        model=model,
        device_map="cpu")
    
    except Exception as exc:
        import logging
        logging.error(exc)

@func.on_execute
async def main(inputs: Inputs, params: Params)-> Outputs:
    if captioner is None:
        raise HTTPException(status_code=500, detail="Model is not loaded yet")
    
    res = captioner(inputs.input_image.to_pil())
    
    return Outputs(caption=res[0]["generated_text"]) # type: ignore
