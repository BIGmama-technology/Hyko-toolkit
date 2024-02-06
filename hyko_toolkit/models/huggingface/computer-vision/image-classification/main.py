from metadata import Inputs, Outputs, Params, StartupParams, func
from transformers import pipeline

classifier = None


@func.on_startup
async def load(startup_params: StartupParams):
    global classifier

    model = startup_params.hugging_face_model
    device_map = startup_params.device_map

    classifier = pipeline(
        "image-classification",
        model=model,
        device_map=device_map,
    )


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    res = classifier(inputs.input_image.to_pil())

    return Outputs(image_class=res[0]["label"])
