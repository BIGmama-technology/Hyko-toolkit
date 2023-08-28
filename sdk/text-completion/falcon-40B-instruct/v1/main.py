import torch
from transformers import AutoTokenizer
import transformers
from fastapi import HTTPException
from pydantic import Field
from hyko_sdk import CoreModel, SDKFunction


func = SDKFunction(
    description="instruct generation model",
    requires_gpu=False,
)

class Inputs(CoreModel):
    prompt : str = Field(..., description="User prompt to falcon-instruct")

class Params(CoreModel):
    system_prompt : str = Field(default=None, description = "system-prompt or system-instruction to falcon-instruct")
    max_length : int = Field(default = 200, description= "Max tokens to generate")
    top_k : int = Field(default=10,description="top_k candidates for each token generation")
    temperature: float = Field(default=0.6, description="Temperature of falcon")
    top_p: float = Field(default=0.6, description="Top P of falcon")

class Outputs(CoreModel):
    generated_text : str = Field(..., description="Generated Text from falcon-instruct")


pipeline = None
tokenizer = None

@func.on_startup
async def load():
    global pipeline
    global tokenizer
    
    if pipeline is not None or tokenizer is not None:
        print("Model already Loaded")
        return
    
    
    model = "tiiuae/falcon-40b-instruct"
    device_map = {
        'transformer.word_embeddings': 0,
        'lm_head': 0,
        'transformer.h.0': 0,
        'transformer.h.1': 0,
        'transformer.h.2': 0,
        'transformer.h.3': 0,
        'transformer.h.4': 0,
        'transformer.h.5': 'cpu',
        'transformer.h.6': 'cpu',
        'transformer.h.7': 1,
        'transformer.h.8': 1,
        'transformer.h.9': 1,
        'transformer.h.10': 1,
        'transformer.h.11': 1,
        'transformer.h.12': 1,
        'transformer.h.13': 'cpu',
        'transformer.h.14': 'cpu',
        'transformer.h.15': 2,
        'transformer.h.16': 2,
        'transformer.h.17': 2,
        'transformer.h.18': 2,
        'transformer.h.19': 2,
        'transformer.h.20': 2,
        'transformer.h.21': 'cpu',
        'transformer.h.22': 'cpu',
        'transformer.h.23': 'cpu',
        'transformer.h.24': 'cpu',
        'transformer.h.25': 'cpu',
        'transformer.h.26': 'cpu',
        'transformer.h.27': 'cpu',
        'transformer.h.28': 'cpu',
        'transformer.h.29': 'cpu',
        'transformer.h.30': 'cpu',
        'transformer.h.31': 'cpu',
        'transformer.h.32': 'cpu',
        'transformer.h.33': 'cpu',
        'transformer.h.34': 'cpu',
        'transformer.h.35': 'cpu',
        'transformer.h.36': 'cpu',
        'transformer.h.37': 'cpu',
        'transformer.h.38': 'cpu',
        'transformer.h.39': 'cpu',
        'transformer.h.40': 'cpu',
        'transformer.h.41': 'cpu',
        'transformer.h.42': 'cpu',
        'transformer.h.43': 'cpu',
        'transformer.h.44': 'cpu',
        'transformer.h.45': 'cpu',
        'transformer.h.46': 'cpu',
        'transformer.h.47': 'cpu',
        'transformer.h.48': 'cpu',
        'transformer.h.49': 'cpu',
        'transformer.h.50': 'cpu',
        'transformer.h.51': 'cpu',
        'transformer.h.52': 'cpu',
        'transformer.h.53': 'cpu',
        'transformer.h.54': 'cpu',
        'transformer.h.55': 'cpu',
        'transformer.h.56': 'cpu',
        'transformer.h.57': 'cpu',
        'transformer.h.58': 'cpu',
        'transformer.h.59': 'cpu',
        'transformer.ln_f': 'cpu'
    }


    tokenizer = AutoTokenizer.from_pretrained(model)

    pipeline = transformers.pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        torch_dtype=torch.bfloat16,
        trust_remote_code=True,
        device_map=device_map,
    )


@func.on_execute
async def main(inputs: Inputs, params: Params):
    if pipeline is None or tokenizer is None:
        raise HTTPException(status_code=500, detail="Model is not loaded yet")
    
    if params.system_prompt:
        prompt = params.system_prompt + "\n" + inputs.prompt
    else:    
        prompt = inputs.prompt
    
    sequences = pipeline(prompt,
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