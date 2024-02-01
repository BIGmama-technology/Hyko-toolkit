import transformers
from metadata import Inputs, Outputs, Params, StartupParams, func


@func.on_startup
async def load(startup_params: StartupParams):
    global translator

    model = startup_params.hugging_face_model
    device_map = startup_params.device_map

    translator = transformers.pipeline(
        task="translation",
        model=model,
        device_map=device_map,
    )


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    res = translator(inputs.original_text)

    return Outputs(translation_text=res[0]["translation_text"])  # type: ignore
