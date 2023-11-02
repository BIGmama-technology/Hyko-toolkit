from fastapi import HTTPException
from pydantic import Field
from hyko_sdk import CoreModel, SDKFunction
import transformers
import os

func = SDKFunction(
    description="Hugging Face summarization",
    requires_gpu=False,
)

class Inputs(CoreModel):
    input_text: str = Field(..., description="text to summarize")

class Params(CoreModel):
    hugging_face_model: str = Field(..., description="Model") # WARNING: DO NOT REMOVE! implementation specific (mathwsch tefham)
    min_length: int = Field(default=30, description="Minimum output length")
    max_length: int = Field(default=130, description="Maximum output length")

class Outputs(CoreModel):
    summary_text: str = Field(..., description="Summary output")


classifier = None

@func.on_startup
async def load():
    global classifier
    
    if classifier is not None:
        print("Model already Loaded")
        return
    
    model = os.getenv("HYKO_HF_SUMMARIZATION_MODEL")
    
    if model is None:
        raise HTTPException(status_code=500, detail="Model env not set")
    
    try:
        classifier = transformers.pipeline(
            task="summarization",
            model=model,
            device_map="auto",
        )
    except Exception as exc:
        import logging
        logging.error(exc)

@func.on_execute
async def main(inputs: Inputs, params: Params)-> Outputs:
    if classifier is None:
        raise HTTPException(status_code=500, detail="Model is not loaded yet")
    
    res = classifier(inputs.input_text, min_length=params.min_length, max_length=params.max_length)
    
    return Outputs(summary_text=res[0]["summary_text"])
