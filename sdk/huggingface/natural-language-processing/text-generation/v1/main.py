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
    hugging_face_model: str = Field(
        ..., description="Model"
    )  # WARNING: DO NOT REMOVE! implementation specific
    device_map: str = Field(
        ..., description="Device map (Auto, CPU or GPU)"
    )  # WARNING: DO NOT REMOVE! implementation specific
    max_length: int = Field(
        default=30, description="maximum number of tokens to generate"
    )


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

    device_map = os.getenv("HYKO_DEVICE_MAP", "auto")

    classifier = transformers.pipeline(
        task="text-generation",
        model=model,
        device_map=device_map,
    )


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    if classifier is None:
        raise HTTPException(status_code=500, detail="Model is not loaded yet")

    res: list[dict[str, str]] = classifier(inputs.input_text, max_length=params.max_length) # type: ignore

    generated_text: str = res[0]["generated_text"]
    
    if len(generated_text) >= len(inputs.input_text):
        return Outputs(generated_text=generated_text[len(inputs.input_text):])
    else:
        return Outputs(generated_text=generated_text)