import transformers
from metadata import Inputs, Outputs, Params, StartupParams, func


@func.on_startup
async def load(startup_params: StartupParams):
    global classifier

    model = startup_params.hugging_face_model
    device_map = startup_params.device_map

    classifier = transformers.pipeline(
        task="zero-shot-classification",
        model=model,
        device_map=device_map,
    )


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    res = classifier(inputs.input_text, candidate_labels=inputs.candidate_labels)

    return Outputs(labels=res["labels"], scores=res["scores"])  # type: ignore
