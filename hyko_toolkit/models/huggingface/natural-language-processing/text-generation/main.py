import transformers
from metadata import Inputs, Outputs, Params, StartupParams, func


@func.on_startup
async def load(startup_params: StartupParams):
    global classifier

    model = startup_params.hugging_face_model
    device_map = startup_params.device_map

    classifier = transformers.pipeline(
        task="text-generation",
        model=model,
        device_map=device_map,
    )


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    res: list[dict[str, str]] = classifier(
        inputs.input_text, max_length=params.max_length
    )  # type: ignore

    generated_text: str = res[0]["generated_text"]

    if len(generated_text) >= len(inputs.input_text):
        return Outputs(generated_text=generated_text[len(inputs.input_text) :])
    else:
        return Outputs(generated_text=generated_text)
