from config import Inputs, Outputs, Params, Audio
import fastapi
from transformers import WhisperProcessor, WhisperForConditionalGeneration
import torch
import torchaudio
from torch.nn import Module
from torch.nn import DataParallel
from torch.types import _TensorOrTensors
from typing import Union

device : torch.device = torch.device("cpu")

# Utils for Whisper
def set_device():
    global device
    if torch.cuda.is_available():
        device = torch.device("cuda:1")
    else:
        device = torch.device("cpu")

def gpu_distribute(
    item: Union[WhisperForConditionalGeneration, _TensorOrTensors]
) -> Union[WhisperForConditionalGeneration, _TensorOrTensors]:
    if torch.cuda.is_available() and torch.cuda.device_count() > 0:
        return DataParallel(item, device_ids = [i for i in range(torch.cuda.device_count())])
    else:
        pass

app = fastapi.FastAPI()
set_device()

processor = WhisperProcessor.from_pretrained("openai/whisper-large-v2")
model = WhisperForConditionalGeneration.from_pretrained(
    "openai/whisper-large-v2"
).to(device)

# model = gpu_distribute(model)

model.config.forced_decoder_ids = None

@app.post("/", response_model=Outputs)
async def main(inputs: Inputs, params: Params):
    waveform, sample_rate = Audio(inputs.input_audio).decode(sampling_rate=16_000)

    input_features = processor.feature_extractor(
        waveform, sampling_rate=16_000, return_tensors="pt"
    ).input_features

    # input_features = gpu_distribute(input_features)
    # print(metadata.streams[0].sample_rate)

    with torch.no_grad():
        output_toks = model.generate(input_features.to(device = device))
        print("Device: ", output_toks.device)
        transcription = processor.batch_decode(
            output_toks, max_new_tokens=10000, skip_special_tokens=True
        )

    print(str(transcription[0]))
    return Outputs(output_text=str(transcription[0]))
