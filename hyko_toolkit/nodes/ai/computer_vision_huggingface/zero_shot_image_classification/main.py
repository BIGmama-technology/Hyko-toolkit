from transformers import pipeline

from .metadata import Inputs, Outputs, Params, node


@node.on_startup
async def load(startup_params: Params):
    global classifier

    model = startup_params.hugging_face_model
    device_map = startup_params.device_map

    classifier = pipeline(
        "zero-shot-image-classification",
        model=model,
        device_map=device_map,
    )


@node.on_call
async def main(inputs: Inputs, params: Params) -> Outputs:
    res = classifier(
        await inputs.input_image.to_pil(),
        candidate_labels=inputs.labels,
        hypothesis_template=params.hypothesis_template,
    )
    labels = [prediction["label"] for prediction in res]
    scores = [prediction["score"] for prediction in res]
    return Outputs(labels=labels, scores=scores)
