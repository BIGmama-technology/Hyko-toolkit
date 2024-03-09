import transformers

from .metadata import Inputs, Outputs, Params, StartupParams, func


@func.on_startup
async def load(startup_params: StartupParams):
    global classifier

    model = startup_params.hugging_face_model
    device_map = startup_params.device_map

    classifier = transformers.pipeline(
        task="text-classification",
        model=model,
        device_map=device_map,
    )


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    res = classifier(inputs.input_text)
    labels = [prediction["label"] for prediction in res]
    scores = [prediction["score"] for prediction in res]

    return Outputs(label=labels, score=scores)  # type: ignore
