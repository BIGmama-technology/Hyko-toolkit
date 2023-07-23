from typing import List
from config import Inputs, Params, Outputs
from fastapi import FastAPI, HTTPException, status
import hyko_sdk.io
import torch
import numpy as np
import math
from transformers import WhisperProcessor, WhisperForConditionalGeneration
from fastapi import HTTPException

app = FastAPI()

model = None
processor = None
device = torch.device("cuda:2") if torch.cuda.is_available() else torch.device('cpu')

@app.post(
    "/load",
    response_model=None,
)
def load():
    global model
    global processor
    if model is not None and processor is not None:
        print("Model loaded already")
        return
    
    processor = WhisperProcessor.from_pretrained("openai/whisper-large-v2")
    model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-large-v2").to(device) # type: ignore
    model.config.forced_decoder_is = None

@app.post(
    "/",
    response_model=Outputs,
)
async def main(inputs: Inputs, params: Params):
    if model is None or processor is None:
        raise HTTPException(status_code=500, detail="Model is not loaded yet")

    await inputs.audio.wait_data()

    if inputs.audio.data is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Received empty audio object",
        )
    
    waveform, sample_rate = inputs.audio.to_ndarray(sampling_rate=16_000)

    transcription = ""
    
    seconds = 30
    segment_size = seconds * sample_rate 
    segments_count = math.ceil(len(waveform) / segment_size)
    waveform_segments = [waveform[segment_size * i: min(segment_size * (i + 1), len(waveform))] for i in range(segments_count)]
    forced_decoder_ids = processor.get_decoder_prompt_ids(language=params.language, task="transcribe")


    for segment in waveform_segments:
        
        input_features = processor.feature_extractor( # type: ignore
            segment, sampling_rate=16_000, return_tensors="pt"
        ).input_features

        with torch.no_grad():
            output_toks = model.generate(input_features.to(device = device), forced_decoder_ids=forced_decoder_ids)
            print("Device: ", output_toks.device) # type: ignore
            transcription_segment = str(processor.batch_decode(
                output_toks, max_new_tokens=10000, skip_special_tokens=True
            )[0])
            print(transcription_segment)
            transcription += transcription_segment

    return Outputs(transcribed_text=transcription)
