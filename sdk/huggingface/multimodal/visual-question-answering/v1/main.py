from fastapi import HTTPException
from pydantic import Field
from hyko_sdk import CoreModel, SDKFunction, Image
from transformers import pipeline
import os


func = SDKFunction(
    description="Hugging Face Image-To-Text Task",
    requires_gpu=False,
)


class Inputs(CoreModel):
    image: Image = Field(..., description="Input image")
    question: str = Field(..., description="Input question")

class Params(CoreModel):
    hugging_face_model: str = Field(
        ..., description="Model"
    )  # WARNING: DO NOT REMOVE! implementation specific
    device_map: str = Field(
        ..., description="Device map (Auto, CPU or GPU)"
    )  # WARNING: DO NOT REMOVE! implementation specific
    top_k: int = Field(default=1, description="Top K")

class Outputs(CoreModel):
    answer: str = Field(..., description="Generated answer")
    score: float = Field(..., description="Confidance score")


vqa_pipeline = None


@func.on_startup
async def load():
    global vqa_pipeline

    if vqa_pipeline is not None:
        print("Model already Loaded")
        return

    model = os.getenv("HYKO_HF_MODEL")

    if model is None:
        raise HTTPException(status_code=500, detail="Model env not set")

    device_map = os.getenv("HYKO_DEVICE_MAP", "auto")
    
    vqa_pipeline = pipeline(
        task="visual-question-answering",
        model=model,
        device_map=device_map,
    )


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    if vqa_pipeline is None:
        raise HTTPException(status_code=500, detail="Model is not loaded yet")

    res = vqa_pipeline(image=inputs.image.to_pil(), question=inputs.question, top_k=params.top_k)

    return Outputs(answer=res[0]["answer"], score=res[0]["score"])  # type: ignore
