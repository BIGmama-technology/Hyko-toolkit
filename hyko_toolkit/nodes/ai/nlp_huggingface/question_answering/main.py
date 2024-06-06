import transformers

from .metadata import Inputs, Outputs, Params, node


@node.on_startup
async def load(startup_params: Params):
    global qa_model

    model = startup_params.hugging_face_model
    device_map = startup_params.device_map

    qa_model = transformers.pipeline(
        model=model,
        device_map=device_map,
    )


@node.on_call
async def main(inputs: Inputs, params: Params) -> Outputs:
    res = qa_model(
        question=inputs.question,
        context=inputs.context,
        doc_strideint=params.doc_stride,
        top_k=params.top_k,
    )  # type: ignore

    return Outputs(
        answer=res["answer"],
        start=res["start"],
        end=res["end"],
        score=res["score"],
    )
