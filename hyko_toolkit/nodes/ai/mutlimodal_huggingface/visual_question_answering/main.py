from transformers import pipeline

from .metadata import Inputs, Outputs, Params, node


@node.on_startup
async def load(startup_params: Params):
    global vqa_pipeline

    model = startup_params.hugging_face_model
    device_map = startup_params.device_map

    vqa_pipeline = pipeline(
        model=model,
        device_map=device_map,
    )


@node.on_call
async def main(inputs: Inputs, params: Params) -> Outputs:
    res = vqa_pipeline(
        image=await inputs.image.to_pil(),
        question=inputs.question,
        top_k=params.top_k,
    )
    answer = [prediction["answer"] for prediction in res]
    scores = [prediction["score"] for prediction in res]
    return Outputs(answer=answer, score=scores)  # type: ignore
