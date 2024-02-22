from metadata import Inputs, Outputs, Params, StartupParams, func
from transformers import pipeline


@func.on_startup
async def load(startup_params: StartupParams):
    global pipe

    model = startup_params.hugging_face_model
    device_map = startup_params.device_map

    pipe = pipeline(
        task="text-generation",
        model=model,
        device_map=device_map,
    )


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    res: list[dict[str, str]] = pipe(
        inputs.input_text,
        do_sample=True,
        max_new_tokens=params.max_new_tokens,
        temperature=params.temperature,
        top_p=params.top_p,
        top_k=params.top_k,
    )  # type: ignore

    generated_text: str = res[0]["generated_text"]
    return Outputs(generated_text=generated_text)
