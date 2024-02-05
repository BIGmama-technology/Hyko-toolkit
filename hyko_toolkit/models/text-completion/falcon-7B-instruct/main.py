import torch
import transformers
from metadata import Inputs, Outputs, Params, StartupParams, func
from transformers import AutoTokenizer


@func.on_startup
async def load(startup_params: StartupParams):
    global pipeline
    global tokenizer

    model = "tiiuae/falcon-7b-instruct"
    tokenizer = AutoTokenizer.from_pretrained(model)

    device_map = {
        "transformer.word_embeddings": 0,
        "lm_head": 0,
        "transformer.h.0": 0,
        "transformer.h.1": 0,
        "transformer.h.2": 0,
        "transformer.h.3": 0,
        "transformer.h.4": 0,
        "transformer.h.5": 0,
        "transformer.h.6": 0,
        "transformer.h.7": 0,
        "transformer.h.8": 0,
        "transformer.h.9": 0,
        "transformer.h.10": 0,
        "transformer.h.11": 0,
        "transformer.h.12": 0,
        "transformer.h.13": 0,
        "transformer.h.14": 0,
        "transformer.h.15": 0,
        "transformer.h.16": 1,
        "transformer.h.17": 1,
        "transformer.h.18": 1,
        "transformer.h.19": 1,
        "transformer.h.20": 1,
        "transformer.h.21": 1,
        "transformer.h.22": 1,
        "transformer.h.23": 1,
        "transformer.h.24": 1,
        "transformer.h.25": 1,
        "transformer.h.26": 1,
        "transformer.h.27": 1,
        "transformer.h.28": 1,
        "transformer.h.29": 1,
        "transformer.h.30": 1,
        "transformer.h.31": 1,
        "transformer.ln_f": 1,
    }
    pipeline = transformers.pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        torch_dtype=torch.bfloat16,
        trust_remote_code=True,
        device_map=device_map,
    )


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
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
        repetition_penalty=params.repetition_penalty,
    )
    output_text = sequences[0]["generated_text"]
    return Outputs(generated_text=output_text)
