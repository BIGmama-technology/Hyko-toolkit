import transformers
from hyko_sdk.models import CoreModel
from metadata import Inputs, Outputs, Params, func


@func.on_startup
async def load(startup_params: Params):
    global classifier

    model = startup_params.hugging_face_model
    device_map = startup_params.device_map

    classifier = transformers.pipeline(
        task="text-classification",
        model=model,
        device_map=device_map,
    )


@func.on_call
async def main(inputs: Inputs, params: CoreModel) -> Outputs:
    res = classifier(inputs.input_text)
    labels = [prediction["label"] for prediction in res]
    scores = [prediction["score"] for prediction in res]

    return Outputs(label=labels, score=scores)
