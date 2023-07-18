from typing import List
from config import Inputs, Params, Outputs
from fastapi import FastAPI, HTTPException, status
import hyko_sdk.io
import torch
import numpy as np
import math
from transformers import WhisperProcessor, WhisperForConditionalGeneration

app = FastAPI()

device = torch.device("cuda:1") if torch.cuda.is_available() else torch.device('cpu')

processor = WhisperProcessor.from_pretrained("openai/whisper-large-v2")
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-large-v2").to(device)
model.config.forced_decoder_is = None



def split_waveform(waveform: np.ndarray, sample_rate: int, seconds:int) -> List[np.ndarray]:
    segment_size = seconds * sample_rate 
    segments_count = math.ceil(len(waveform) / segment_size)
    return [waveform[segment_size * i: min(segment_size * (i + 1), len(waveform))] for i in range(segments_count)]
    

@app.post(
    "/",
    response_model=Outputs,
)
async def main(inputs: Inputs, params: Params):

    await inputs.audio.wait_data()

    if inputs.audio.data is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Received empty audio object",
        )
    
    waveform, sample_rate = inputs.audio.decode(sampling_rate=16_000)

    transcription = ""

    for w in split_waveform(waveform, sample_rate, 30):
        
        input_features = processor.feature_extractor(
            w, sampling_rate=16_000, return_tensors="pt"
        ).input_features

        with torch.no_grad():
            output_toks = model.generate(input_features.to(device = device))
            print("Device: ", output_toks.device)
            transcription_segment = str(processor.batch_decode(
                output_toks, max_new_tokens=10000, skip_special_tokens=True
            )[0])
            print(transcription_segment)
            transcription += transcription_segment

    return Outputs(transcribed_text=hyko_sdk.io.String(transcription))
