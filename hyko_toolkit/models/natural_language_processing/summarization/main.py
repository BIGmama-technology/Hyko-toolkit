import transformers
from metadata import Inputs, Outputs, Params, StartupParams, func


@func.on_startup
async def load(startup_params: StartupParams):
    global summarizer

    model = startup_params.hugging_face_model
    device_map = startup_params.device_map

    summarizer = transformers.pipeline(
        task="summarization",
        model=model,
        device_map=device_map,
    )


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    res = summarizer(
        inputs.input_text,
        do_sample=True,
        min_length=params.min_length,
        max_length=params.max_length,
        temperature=params.temperature,
        top_p=params.top_p,
        top_k=params.top_k,
    )

    return Outputs(summary_text=res[0]["summary_text"])  # type: ignore
