import math
import os

import torch
from fastapi.exceptions import HTTPException
from pydantic import Field
from transformers import WhisperForConditionalGeneration, WhisperProcessor

from hyko_sdk.function import SDKFunction
from hyko_sdk.io import Audio
from hyko_sdk.metadata import CoreModel

func = SDKFunction(
    description="OpenAI's Audio Transcription model (Non API)",
    requires_gpu=True,
)


class Inputs(CoreModel):
    audio: Audio = Field(..., description="Input audio that will be transcribed")


class Params(CoreModel):
    language: str = Field(default="en", description="The language of the audio")
    device_map: str = Field(
        ..., description="Device map (Auto, CPU or GPU)"
    )  # WARNING: DO NOT REMOVE! implementation specific


class Outputs(CoreModel):
    transcribed_text: str = Field(..., description="Generated transcription text")


model = None
processor = None


@func.on_startup
async def load():
    global model
    global processor

    if model is not None and processor is not None:
        print("Model loaded already")
        return

    if not torch.cuda.is_available():
        raise Exception("Machine does not have cuda capable devices")

    device = os.getenv("HYKO_DEVICE_MAP", "cuda")

    processor = WhisperProcessor.from_pretrained("openai/whisper-large-v2")
    model = WhisperForConditionalGeneration.from_pretrained(
        "openai/whisper-large-v2"
    ).to(device)  # type: ignore
    model.config.forced_decoder_is = None


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    if model is None or processor is None:
        raise HTTPException(status_code=500, detail="Model is not loaded yet")

    waveform, sample_rate = inputs.audio.to_ndarray(sampling_rate=16_000)
    waveform = torch.unsqueeze(torch.tensor(waveform), 0).numpy()

    transcription = ""

    seconds = 30
    segment_size = seconds * sample_rate
    segments_count = math.ceil(len(waveform) / segment_size)
    waveform_segments = [
        waveform[segment_size * i : min(segment_size * (i + 1), len(waveform))]
        for i in range(segments_count)
    ]
    forced_decoder_ids = processor.get_decoder_prompt_ids(language=params.language)
    device = os.getenv("HYKO_DEVICE_MAP", "cuda")

    for segment in waveform_segments:
        input_features = processor.feature_extractor(  # type: ignore
            segment[0], sampling_rate=16_000, return_tensors="pt"
        ).input_features

        with torch.no_grad():
            output_toks = model.generate(
                input_features.to(device=device), forced_decoder_ids=forced_decoder_ids
            )
            print("Device: ", output_toks.device)  # type: ignore
            transcription_segment = str(
                processor.batch_decode(
                    output_toks, max_new_tokens=10000, skip_special_tokens=True
                )[0]
            )
            print(transcription_segment)
            transcription += transcription_segment

    return Outputs(transcribed_text=transcription)
