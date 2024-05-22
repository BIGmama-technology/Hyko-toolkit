from hyko_sdk.io import Image
from hyko_sdk.models import CoreModel
from transformers import pipeline

from .metadata import Inputs, Outputs, Params, func


@func.on_startup
async def load(startup_params: Params):
    global estimator

    model = startup_params.hugging_face_model
    device_map = startup_params.device_map

    estimator = pipeline(
        "depth-estimation",
        model=model,
        device_map=device_map,
    )


@func.on_call
async def main(inputs: Inputs, params: CoreModel) -> Outputs:
    res = estimator(await inputs.input_image.to_pil())
    depth_map = await Image.from_pil(res["depth"])

    return Outputs(depth_map=depth_map)  # type: ignore
