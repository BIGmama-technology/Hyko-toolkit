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
    if err_:
        raise fastapi.HTTPException(status_code=500, detail=err_.json())
    
    input_features = processor.feature_extractor(
        waveform, sampling_rate=16_000, return_tensors="pt"
    ).input_features 
    
    # print(metadata.streams[0].sample_rate)

    with torch.no_grad():
        output_toks = model.generate(input_features.cuda())
        print(output_toks)
        transcription = processor.batch_decode(
            output_toks, max_new_tokens=10000, skip_special_tokens=True
        )
        print(transcription)

    return Outputs(output_text=str(transcription))
