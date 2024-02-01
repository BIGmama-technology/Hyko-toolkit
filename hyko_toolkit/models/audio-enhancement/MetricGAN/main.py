import shutil

import torch
from metadata import Inputs, Outputs, Params, StartupParams, func
from speechbrain.pretrained import SpectralMaskEnhancement

from hyko_sdk.io import Audio


@func.on_startup
async def load(startup_params: StartupParams):
    global model

    model = SpectralMaskEnhancement.from_hparams(
        source="speechbrain/metricgan-plus-voicebank",
        device=startup_params.device_map,
    )


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
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
