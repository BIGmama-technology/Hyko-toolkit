from hyko_sdk.io import Image
from hyko_sdk.models import CoreModel
from metadata import Inputs, Outputs, StartupParams, func
from transformers import pipeline


@func.on_startup
async def load(startup_params: StartupParams):
    global estimator

    model = startup_params.hugging_face_model
    device_map = startup_params.device_map

    estimator = pipeline(
        "depth-estimation",
        model=model,
        device_map=device_map,
    )


@func.on_execute
async def main(inputs: Inputs, params: CoreModel) -> Outputs:
    res = estimator(inputs.input_image.to_pil())
    depth_map = Image.from_pil(res["depth"])

    return Outputs(depth_map=depth_map)  # type: ignore
