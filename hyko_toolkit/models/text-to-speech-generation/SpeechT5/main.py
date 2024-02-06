import torch
from datasets import load_dataset
from fastapi import HTTPException
from metadata import Inputs, Outputs, Params, StartupParams, func
from transformers import SpeechT5ForTextToSpeech, SpeechT5HifiGan, SpeechT5Processor

from hyko_sdk.io import Audio


@func.on_startup
async def load(startup_params: StartupParams):
    global model
    global processor
    global vocoder
    global device

    device = startup_params.device_map
    processor = SpeechT5Processor.from_pretrained("microsoft/speecht5_tts")
    model = SpeechT5ForTextToSpeech.from_pretrained("microsoft/speecht5_tts")
    vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan")


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    if model is None or processor is None:
        raise HTTPException(status_code=500, detail="Model is not loaded yet")

    inputs = processor(text=inputs.text, return_tensors="pt")

    embeddings_dataset = load_dataset(
        "Matthijs/cmu-arctic-xvectors", split="validation"
    )
    speaker_embeddings = torch.tensor(embeddings_dataset[7306]["xvector"]).unsqueeze(0)

    speech = model.generate_speech(
        inputs["input_ids"], speaker_embeddings, vocoder=vocoder
    )

    speech_ndarray = speech.detach().cpu().numpy()

    audio = Audio.from_ndarray(arr=speech_ndarray, sampling_rate=16_000)

    return Outputs(audio=audio)
