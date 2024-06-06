from hyko_sdk.io import Audio
from transformers import pipeline

from .metadata import Inputs, Outputs, Params, node

synthesizer = None


@node.on_startup
async def load(startup_params: Params):
    global synthesizer

    model = startup_params.hugging_face_model
    device_map = startup_params.device_map

    synthesizer = pipeline("text-to-speech", model=model, device_map=device_map)


@node.on_call
async def main(inputs: Inputs, params: Params) -> Outputs:
    result_audio = synthesizer(
        inputs=inputs.text,
        generate_kwargs={
            "do_sample": True,
            "top_k": params.top_k,
            "top_p": params.top_p,
            "temperature": params.temperature,
        },
    )  # type: ignore
    result_audio = await Audio.from_ndarray(
        result_audio["audio"],
        sampling_rate=result_audio["sampling_rate"],
    )

    return Outputs(speech=result_audio)  # type: ignore
