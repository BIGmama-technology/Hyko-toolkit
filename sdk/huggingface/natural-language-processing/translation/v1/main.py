from fastapi import HTTPException
from pydantic import Field
from hyko_sdk import CoreModel, SDKFunction
import transformers
import os

func = SDKFunction(
    description="Hugging Face translation task",
    requires_gpu=False,
)

class Inputs(CoreModel):
    original_text: str = Field(..., description="Original input text")

class Params(CoreModel):
    hugging_face_model: str = Field(..., description="Model") # WARNING: DO NOT REMOVE! implementation specific

class Outputs(CoreModel):
    translation_text: str = Field(..., description="Translated text")


translator = None

@func.on_startup
async def load():
    global translator
    
    if translator is not None:
        print("Model already Loaded")
        return
    
    model = os.getenv("HYKO_HF_MODEL")
    
    if model is None:
        raise HTTPException(status_code=500, detail="Model env not set")
    
    try:
        translator = transformers.pipeline(
            task="translation",
            model=model,
            device_map="cpu",
        )
    except Exception as exc:
        import logging
        logging.error(exc)

@func.on_execute
async def main(inputs: Inputs, params: Params)-> Outputs:
    if translator is None:
        raise HTTPException(status_code=500, detail="Model is not loaded yet")
    
    res = translator(inputs.original_text)
    
    return Outputs(translation_text=res[0]["translation_text"]) # type: ignore
