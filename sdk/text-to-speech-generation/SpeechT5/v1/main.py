import torch
from datasets import load_dataset
from fastapi import HTTPException
from pydantic import Field
from transformers import SpeechT5ForTextToSpeech, SpeechT5HifiGan, SpeechT5Processor

from hyko_sdk.function import SDKFunction
from hyko_sdk.io import Audio
from hyko_sdk.metadata import CoreModel

func = SDKFunction(
    description="Generate audio from English text input",
    requires_gpu=False,
)


class Inputs(CoreModel):
    text: str = Field(
        ..., description="English text input provided by the user for speech generation"
    )


class Params(CoreModel):
    pass


class Outputs(CoreModel):
    audio: Audio = Field(
        ...,
        description="Generated audio containing the speech corresponding to the provided text",
    )


model = None
processor = None
vocoder = None

device = torch.device("cuda:0") if torch.cuda.is_available() else torch.device("cpu")


@func.on_startup
async def load():
    global model
    global processor
    global vocoder
    if model is not None and processor is not None:
        print("Model loaded already")
        return

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
