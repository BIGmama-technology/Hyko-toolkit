from config import Inputs, Outputs, Params
import fastapi
from transformers import WhisperProcessor, WhisperForConditionalGeneration, audio_utils
import numpy as np
import torch
import base64
import torchaudio

# import ffmpeg
import io
import soundfile as sf

app = fastapi.FastAPI()

processor = WhisperProcessor.from_pretrained("openai/whisper-small")
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-small")
model.config.forced_decoder_ids = None

@app.post("/", response_model=Outputs)
async def main(inputs: Inputs, params: Params):
    audio_bytes = base64.urlsafe_b64decode(inputs.input_audio.split(",")[1])
    print(type(inputs.input_audio))
    input_audio_arr, metadata, err_  = inputs.input_audio.decode() 
    if err_:
     raise fastapi.HTTPException(status_code=500, details=err_.json())
    # print(data, "\n", sample_rate)
    #  = np.frombuffer(audio_bytes, dtype=np.float64)
    # print("Numpy Audio: ", audio_)
    print(input_audio_arr, "\n", metadata)
    # audio_ = torch.from_numpy(data)
    print("Numpy Audio Shape: ", audio_.shape)
    input_features = processor.feature_extractor(audio_, sampling_rate = 16_000, return_tensors="pt")
    print("Input Features: ", input_features)
    # return Outputs(output_text=None)
    return Outputs(output_text = str(input_features))