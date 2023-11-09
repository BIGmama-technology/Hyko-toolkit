from fastapi import HTTPException
from pydantic import Field
from hyko_sdk import CoreModel, SDKFunction
import transformers
import os

func = SDKFunction(
    description="Hugging Face Question Answering task",
    requires_gpu=False,
)

class Inputs(CoreModel):
    question: str = Field(..., description="Input question")
    context: str = Field(..., description="Context from which to answer the question")

class Params(CoreModel):
    hugging_face_model: str = Field(..., description="Model") # WARNING: DO NOT REMOVE! implementation specific

class Outputs(CoreModel):
    answer: str = Field(..., description="Answer to the question")
    start: int = Field(..., description="Start index")
    end: int = Field(..., description="End index")
    score: float = Field(..., description="Score of the answer")
    


qa_model = None

@func.on_startup
async def load():
    global qa_model
    
    if qa_model is not None:
        print("Model already Loaded")
        return
    
    model = os.getenv("HYKO_HF_MODEL")
    
    if model is None:
        raise HTTPException(status_code=500, detail="Model env not set")
    
    try:
        qa_model = transformers.pipeline(
            task="question-answering",
            model=model,
            device_map="cpu",
        )
    except Exception as exc:
        import logging
        logging.error(exc)

@func.on_execute
async def main(inputs: Inputs, params: Params)-> Outputs:
    if qa_model is None:
        raise HTTPException(status_code=500, detail="Model is not loaded yet")
    
    res = qa_model(question=inputs.question, context=inputs.context) # type: ignore
    
    return Outputs(
        answer=res["answer"], # type: ignore
        start=res["start"], # type: ignore
        end=res["end"], # type: ignore
        score=res["score"], # type: ignore
    )
