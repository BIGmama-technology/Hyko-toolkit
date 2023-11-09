from fastapi import HTTPException
from pydantic import Field
from hyko_sdk import CoreModel, SDKFunction
import transformers
import os

func = SDKFunction(
    description="Hugging Face text generation",
    requires_gpu=False,
)

class Inputs(CoreModel):
    input_text: str = Field(..., description="input text")

class Params(CoreModel):
    hugging_face_model: str = Field(..., description="Model") # WARNING: DO NOT REMOVE! implementation specific
    max_length: int = Field(default=30, description="maximum number of tokens to generate")

class Outputs(CoreModel):
    generated_text: str = Field(..., description="Completion text")


classifier = None

@func.on_startup
async def load():
    global classifier
    
    if classifier is not None:
        print("Model already Loaded")
        return
    
    model = os.getenv("HYKO_HF_MODEL")
    
    if model is None:
        raise HTTPException(status_code=500, detail="Model env not set")
    
    try:
        classifier = transformers.pipeline(
            task="text-generation",
            model=model,
            device_map="cpu",
        )
    except Exception as exc:
        import logging
        logging.error(exc)

@func.on_execute
async def main(inputs: Inputs, params: Params)-> Outputs:
    if classifier is None:
        raise HTTPException(status_code=500, detail="Model is not loaded yet")
    
    res = classifier(inputs.input_text, max_length=params.max_length)

    return Outputs(generated_text=res[0]["generated_text"]) # type: ignore
