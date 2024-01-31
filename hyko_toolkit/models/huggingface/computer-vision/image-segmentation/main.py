"""
TODO handle the output of segmentation, now only one mask is supported and is
returned as a PIL image.
"""

from metadata import Inputs, Outputs, Params, StartupParams, func
from transformers import pipeline

from hyko_sdk.io import Image

segmenter = None


@func.on_startup
async def load(params: StartupParams):
    global segmenter

    model = params.hugging_face_model
    device_map = params.device_map

    segmenter = pipeline(
        "image-segmentation",
        model=model,
        device_map=device_map,
    )


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    res = segmenter(inputs.input_image.to_pil())
    mask = Image.from_pil(res[0]["mask"])

    return Outputs(mask=mask)
