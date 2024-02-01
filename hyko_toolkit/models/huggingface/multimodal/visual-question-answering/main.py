from metadata import Inputs, Outputs, Params, StartupParams, func
from transformers import pipeline


@func.on_startup
async def load(startup_params: StartupParams):
    global vqa_pipeline

    model = startup_params.hugging_face_model
    device_map = startup_params.device_map

    vqa_pipeline = pipeline(
        task="visual-question-answering",
        model=model,
        device_map=device_map,
    )


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    res = vqa_pipeline(
        image=inputs.image.to_pil(), question=inputs.question, top_k=params.top_k
    )

    return Outputs(answer=res[0]["answer"], score=res[0]["score"])  # type: ignore
