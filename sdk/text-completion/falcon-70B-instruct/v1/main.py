from fastapi import HTTPException
from pydantic import Field
from hyko_sdk import CoreModel, SDKFunction
import transformers
import subprocess

func = SDKFunction(
    description="Falcon 70B instruct",
    requires_gpu=False,
)


class Inputs(CoreModel):
    input_text: str = Field(..., description="input text")


class Params(CoreModel):
    max_length: int = Field(
        default=30, description="maximum number of tokens to generate"
    )


class Outputs(CoreModel):
    generated_text: str = Field(..., description="Completion text")


generator = None


@func.on_startup
async def load():
    global generator

    if generator is not None:
        print("Model already Loaded")
        return
    
    subprocess.run(
        "git clone https://huggingface.co/upstage/Llama-2-70b-instruct".split(' ')
    )
    
    generator = transformers.pipeline(
        model="Llama-2-70b-instruct",
        device_map="auto",
    )


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    if generator is None:
        raise HTTPException(status_code=500, detail="Model is not loaded yet")

    res = generator(inputs.input_text, max_length=params.max_length)

    return Outputs(generated_text=res[0]["generated_text"])  # type: ignore
