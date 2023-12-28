import shutil

import torch
from fastapi import HTTPException
from pydantic import Field
from speechbrain.pretrained import SpectralMaskEnhancement

from hyko_sdk.function import SDKFunction
from hyko_sdk.io import Audio
from hyko_sdk.metadata import CoreModel

func = SDKFunction(
    description="Enhance the quality of an audio recording. This model is designed to reduce noise and enhance the clarity of an audio file",
    requires_gpu=False,
)


class Inputs(CoreModel):
    audio: Audio = Field(..., description="Audio input by the user for enhancement")


class Params(CoreModel):
    pass


class Outputs(CoreModel):
    enhanced: Audio = Field(..., description="Enhanced audio after processing")


model = None
tokenizer = None
device = torch.device("cuda:0") if torch.cuda.is_available() else torch.device("cpu")


@func.on_startup
async def load():
    global model
    global tokenizer
    if model is not None and tokenizer is not None:
        print("Model loaded already")
        return

    model = SpectralMaskEnhancement.from_hparams(
        source="speechbrain/metricgan-plus-voicebank"
    )


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    if model is None:
        raise HTTPException(status_code=500, detail="Model is not loaded yet")

    waveform, sample_rate = inputs.audio.to_ndarray()
    waveform = torch.unsqueeze(torch.tensor(waveform), 0)

    with torch.no_grad():
        enhanced = model.enhance_batch(waveform, lengths=torch.tensor([1.0]))

    enhanced_ndarray = enhanced.detach().cpu().numpy()

    enhanced_audio = Audio.from_ndarray(
        arr=enhanced_ndarray[0], sampling_rate=sample_rate
    )

    return Outputs(enhanced=enhanced_audio)


@func.on_shutdown
async def end():
    shutil.rmtree("./pretrained_models")
