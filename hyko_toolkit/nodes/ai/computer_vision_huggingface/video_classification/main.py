import os

from transformers import pipeline

from .metadata import Inputs, Outputs, Params, func


@func.on_startup
async def load(startup_params: Params):
    global segmenter

    model = startup_params.hugging_face_model
    device_map = startup_params.device_map

    segmenter = pipeline(
        "video-classification",
        model=model,
        device_map=device_map,
    )


@func.on_call
async def main(inputs: Inputs, params: Params) -> Outputs:
    _, ext = os.path.splitext(inputs.input_video.get_name())

    with open(f"/app/video.{ext}", "wb") as f:
        f.write(await inputs.input_video.get_data())

    res = segmenter(
        f"/app/video.{ext}",
        top_k=params.top_k,
        frame_sampling_rate=params.frame_sampling_rate,
    )
    labels = [prediction["label"] for prediction in res]
    scores = [prediction["score"] for prediction in res]
    return Outputs(labels=labels, scores=scores)
