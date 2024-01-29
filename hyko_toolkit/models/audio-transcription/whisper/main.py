import math

import torch
from metadata import Inputs, Outputs, Params, StartupParams, func
from transformers import WhisperForConditionalGeneration, WhisperProcessor


@func.on_startup
async def load(startup_params: StartupParams):
    global model
    global processor
    global device

    device = startup_params.device_map

    processor = WhisperProcessor.from_pretrained("openai/whisper-tiny")
    model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-tiny").to(
        device
    )
    model.config.forced_decoder_is = None


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
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

    for segment in waveform_segments:
        input_features = processor.feature_extractor(  # type: ignore
            segment[0], sampling_rate=16_000, return_tensors="pt"
        ).input_features

        with torch.no_grad():
            output_toks = model.generate(
                input_features.to(device=device), forced_decoder_ids=forced_decoder_ids
            )
            transcription_segment = str(
                processor.batch_decode(
                    output_toks, max_new_tokens=10000, skip_special_tokens=True
                )[0]
            )
            transcription += transcription_segment

    return Outputs(transcribed_text=transcription)


print(func.dump_metadata())
