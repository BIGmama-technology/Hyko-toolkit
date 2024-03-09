"""
TODO handle the output of segmentation, now only one mask is supported and is
returned as a PIL image.
"""
import numpy as np
from PIL import Image as PILLImage
from transformers import pipeline

from hyko_sdk.io import Image

from .metadata import Inputs, Outputs, Params, StartupParams, func

segmenter = None


@func.on_startup
async def load(startup_params: StartupParams):
    global segmenter

    model = startup_params.hugging_face_model
    device_map = startup_params.device_map

    segmenter = pipeline(
        "image-segmentation",
        model=model,
        device_map=device_map,
    )


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    res = segmenter(
        inputs.input_image.to_pil(),
        threshold=params.threshold,
        mask_threshold=params.mask_threshold,
        overlap_mask_area_threshold=params.overlap_mask_area_threshold,
    )
    masks = [mask["mask"] for mask in res]
    mask_arrays = [np.array(mask) for mask in masks]
    stacked_mask = np.hstack(mask_arrays)
    stacked_image = PILLImage.fromarray(stacked_mask)
    mask = Image.from_pil(stacked_image)
    return Outputs(mask=mask)
