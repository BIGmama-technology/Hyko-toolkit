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
    res = captioner(
        await inputs.image.to_pil(),
        generate_kwargs={
            "do_sample": True,
            "top_k": params.top_k,
            "top_p": params.top_p,
            "temperature": params.temperature,
            "max_new_tokens": params.max_new_tokens,
        },
    )
    return Outputs(generated_text=res[0]["generated_text"])  # type: ignore
