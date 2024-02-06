import transformers
from metadata import Inputs, Outputs, Params, StartupParams, func


@func.on_startup
async def load(startup_params: StartupParams):
    global classifier

    model = startup_params.hugging_face_model
    device_map = startup_params.device_map

    classifier = transformers.pipeline(
        task="summarization",
        model=model,
        device_map=device_map,
    )


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    res = classifier(
        inputs.input_text, min_length=params.min_length, max_length=params.max_length
    )

    return Outputs(summary_text=res[0]["summary_text"])  # type: ignore
