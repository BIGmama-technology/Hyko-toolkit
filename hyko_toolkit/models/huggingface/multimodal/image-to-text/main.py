from metadata import Inputs, Outputs, Params, StartupParams, func
from transformers import pipeline


@func.on_startup
async def load(startup_params: StartupParams):
    global captioner

    model = startup_params.hugging_face_model
    device_map = startup_params.device_map

    captioner = pipeline(
        task="image-to-text",
        model=model,
        device_map=device_map,
    )


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    res = captioner(inputs.image.to_pil())

    return Outputs(generated_text=res[0]["generated_text"])  # type: ignore
