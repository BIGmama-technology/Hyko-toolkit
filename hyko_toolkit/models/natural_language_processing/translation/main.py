import transformers

from .metadata import Inputs, Outputs, Params, func


@func.on_startup
async def load(startup_params: Params):
    global translator

    model = startup_params.hugging_face_model
    device_map = startup_params.device_map

    translator = transformers.pipeline(
        task="translation",
        model=model,
        device_map=device_map,
    )


@func.on_call
async def main(inputs: Inputs, params: Params) -> Outputs:
    res = translator(
        inputs.original_text,
        do_sample=True,
        max_new_tokens=params.max_new_tokens,
        temperature=params.temperature,
        top_p=params.top_p,
        top_k=params.top_k,
        src_lang=params.src_lang,
        tgt_lang=params.tgt_lang,
    )

    return Outputs(translation_text=res[0]["translation_text"])  # type: ignore
