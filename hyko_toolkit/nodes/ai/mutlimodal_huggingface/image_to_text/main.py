from transformers import pipeline

from .metadata import Inputs, Outputs, Params, node


@node.on_startup
async def load(startup_params: Params):
    global captioner

    model = startup_params.hugging_face_model
    device_map = startup_params.device_map

    captioner = pipeline(
        model=model,
        device_map=device_map,
    )


@node.on_call
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
