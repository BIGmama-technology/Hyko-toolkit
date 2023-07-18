import fastapi
from config import Inputs, Params, Outputs
import torch
from transformers import AutoTokenizer
import transformers
from fastapi import HTTPException

app = fastapi.FastAPI()

pipeline = None
tokenizer = None

@app.post("/load", response_model=None)
def load():
    global pipeline
    global tokenizer
    
    if pipeline is not None or tokenizer is not None:
        print("Model already Loaded")
        return
    
    
    model = "tiiuae/falcon-7b-instruct"
    tokenizer = AutoTokenizer.from_pretrained(model)


    device_map = {
        'transformer.word_embeddings': 0,
        'lm_head': 0,
        'transformer.h.0': 0,
        'transformer.h.1': 0,
        'transformer.h.2': 0,
        'transformer.h.3': 0,
        'transformer.h.4': 0,
        'transformer.h.5': 0,
        'transformer.h.6': 0,
        'transformer.h.7': 0,
        'transformer.h.8': 0,
        'transformer.h.9': 0,
        'transformer.h.10': 0,
        'transformer.h.11': 0,
        'transformer.h.12': 0,
        'transformer.h.13': 0,
        'transformer.h.14': 0,
        'transformer.h.15': 0,
        'transformer.h.16': 2,
        'transformer.h.17': 2,
        'transformer.h.18': 2,
        'transformer.h.19': 2,
        'transformer.h.20': 2,
        'transformer.h.21': 2,
        'transformer.h.22': 2,
        'transformer.h.23': 2,
        'transformer.h.24': 2,
        'transformer.h.25': 2,
        'transformer.h.26': 2,
        'transformer.h.27': 2,
        'transformer.h.28': 2,
        'transformer.h.29': 2,
        'transformer.h.30': 2,
        'transformer.h.31': 2,
        'transformer.ln_f': 2
    }
    pipeline = transformers.pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        torch_dtype=torch.bfloat16,
        trust_remote_code=True,
        device_map=device_map,
    )


@app.post("/", response_model=Outputs)
async def main(inputs: Inputs, params: Params):
    if pipeline is None or tokenizer is None:
        raise HTTPException(status_code=500, detail="Model is not loaded yet")
    
    if params.system_prompt:
        prompt = params.system_prompt + "\n" + inputs.prompt
    else:    
        prompt = inputs.prompt
    
    sequences = pipeline(
            prompt,
            max_length=params.max_length,
            do_sample=True,
            top_k=params.top_k,
            num_return_sequences=1,
            eos_token_id=tokenizer.eos_token_id,
            return_full_text=False,
            temperature=params.temperature,
            top_p=params.top_p,
            repetition_penalty=0.5
        )
    output_text = sequences[0]['generated_text']
    return Outputs(generated_text=output_text)