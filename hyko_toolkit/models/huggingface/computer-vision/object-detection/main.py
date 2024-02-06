from metadata import Inputs, Outputs, Params, StartupParams, func
from transformers import pipeline


@func.on_startup
async def load(startup_params: StartupParams):
    global detector

    model = startup_params.hugging_face_model
    device_map = startup_params.device_map

    detector = pipeline(
        "object-detection",
        model=model,
        device_map=device_map,
    )


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    res = detector(inputs.input_image.to_pil())
    if len(res) == 0:
        summary = "No objects detected"
    else:
        summary = str(res)

    return Outputs(summary=summary)  # type: ignore
