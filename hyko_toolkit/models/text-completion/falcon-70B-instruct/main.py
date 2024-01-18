import transformers
from fastapi import HTTPException
from metadata import Inputs, Outputs, Params, func

generator = None


@func.on_startup
async def load():
    global generator

    if generator is not None:
        print("Model already Loaded")
        return

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
