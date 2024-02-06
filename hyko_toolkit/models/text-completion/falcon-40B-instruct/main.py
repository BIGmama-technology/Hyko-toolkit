import torch
import transformers
from metadata import Inputs, Outputs, Params, StartupParams, func
from transformers import AutoTokenizer


@func.on_startup
async def load(startup_params: StartupParams):
    global pipeline
    global tokenizer

    model = "tiiuae/falcon-40b-instruct"

    tokenizer = AutoTokenizer.from_pretrained(model)

    pipeline = transformers.pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        torch_dtype=torch.bfloat16,
        trust_remote_code=True,
        device_map="auto",
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
        repetition_penalty=0.5,
    )
    output_text = sequences[0]["generated_text"]
    return Outputs(generated_text=output_text)
