from fastapi.exceptions import HTTPException
import torch
from transformers import pipeline
from pydantic import Field
from hyko_sdk import CoreModel, SDKFunction


func = SDKFunction(
    description="Predicts a future value based on historical data",
    requires_gpu=False,
)

class Inputs(CoreModel):
    text: str = Field(..., description="Input text (16k tokens max context size)")

class Params(CoreModel):
    max_length: int = Field(..., description="Input text (16k tokens max context size)")
    min_length: int = Field(..., description="Input text (16k tokens max context size)")
    do_sample: bool = Field(..., description="Input text (16k tokens max context size)")
    
class Outputs(CoreModel):
    summary: str = Field(..., description="Summarized text")

model_pipeline = None
device = torch.device("cuda:0") if torch.cuda.is_available() else torch.device('cpu')



@func.on_startup
async def load():
    global model_pipeline
    if model_pipeline is not None:
        print("Model loaded already")
        return
    
    model_pipeline = pipeline("summarization", model="facebook/bart-large-cnn", device_map=device)

@func.on_execute
async def main(inputs: Inputs, params: Params):

    if model_pipeline is None:
        raise HTTPException(status_code=500, detail="Model is not loaded yet")
    
    summary_list= model_pipeline(inputs.text, params.max_length, params.min_length, params.do_sample)
    summary = summary_list[0]['summary_text']
    return Outputs(summary=summary)

