"""
TODO handle the output of segmentation, now only one mask is supported and is
returned as a PIL image.
"""
import numpy as np
from hyko_sdk.io import Image
from PIL import Image as PILLImage
from transformers import pipeline

from .metadata import Inputs, Outputs, Params, node

segmenter = None


@node.on_startup
async def load(startup_params: Params):
    global segmenter

    model = startup_params.hugging_face_model
    device_map = startup_params.device_map

    segmenter = pipeline(
        "image-segmentation",
        model=model,
        device_map=device_map,
    )


@node.on_call
async def main(inputs: Inputs, params: Params) -> Outputs:
    res = segmenter(
        await inputs.input_image.to_pil(),
        threshold=params.threshold,
        mask_threshold=params.mask_threshold,
        overlap_mask_area_threshold=params.overlap_mask_area_threshold,
    )
    masks = [mask["mask"] for mask in res]
    mask_arrays = [np.array(mask) for mask in masks]
    stacked_mask = np.hstack(mask_arrays)
    stacked_image = PILLImage.fromarray(stacked_mask)
    mask = await Image.from_pil(stacked_image)
    return Outputs(mask=mask)
