from config import Inputs, Outputs, Params, Audio
import fastapi
from transformers import WhisperProcessor, WhisperForConditionalGeneration
import torch

app = fastapi.FastAPI()

processor = WhisperProcessor.from_pretrained("openai/whisper-large-v2")
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-large-v2").cuda()
model.config.forced_decoder_ids = None


@app.post("/", response_model=Outputs)
async def main(inputs: Inputs, params: Params):
    waveform, sample_rate, err_ = Audio(inputs.input_audio).decode(sampling_rate = 16_000)
    if err_ :
        raise fastapi.HTTPException(status_code=500, detail=err_.json())
    if waveform is None or sample_rate is None:
        raise fastapi.HTTPException(status_code=500, detail="Unexpected Error")
    
    input_features = processor.feature_extractor(
        waveform[0], sampling_rate=16_000, return_tensors="pt"
    ).input_features 
    
    # print(metadata.streams[0].sample_rate)

    with torch.no_grad():
        output_toks = model.generate(input_features.cuda())
        transcription = processor.batch_decode(
            output_toks, max_new_tokens=10000, skip_special_tokens=True
        )

    return Outputs(output_text=str(transcription))
