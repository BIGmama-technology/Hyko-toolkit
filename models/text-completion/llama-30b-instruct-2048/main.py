import torch
from fastapi import HTTPException
from metadata import Inputs, Outputs, Params, func
from transformers import TextStreamer
from transformers.models.llama.modeling_llama import LlamaForCausalLM
from transformers.models.llama.tokenization_llama_fast import LlamaTokenizerFast

tokenizer = None
model = None


@func.on_startup
async def load():
    global tokenizer
    global model

    if tokenizer is not None or model is not None:
        print("Model already Loaded")
        return

    tokenizer = LlamaTokenizerFast.from_pretrained("upstage/llama-30b-instruct-2048")
    model = LlamaForCausalLM.from_pretrained(
        "upstage/llama-30b-instruct-2048",
        device_map="auto",
        torch_dtype=torch.float16,
        load_in_8bit=True,
        rope_scaling={
            "type": "dynamic",
            "factor": 2,
        },  # allows handling of longer inputs
    )


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    if tokenizer is None or model is None:
        raise HTTPException(status_code=500, detail="Model not loaded yet")

    prompt = ""

    if params.system_prompt:
        prompt = (
            "### System:\n"
            + params.system_prompt
            + "\n### User:\n"
            + inputs.prompt
            + "\n### Assistant:\n"
        )
    else:
        prompt = (
            "### System:\n"
            + "You are a useful assistant"
            + "\n### User:\n"
            + inputs.prompt
            + "\n### Assistant:\n"
        )

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    streamer = TextStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)

    print(f"type(tokenizer): {type(tokenizer)}")
    print(f"type(model): {type(model)}")

    output = model.generate(
        **inputs, streamer=streamer, use_cache=True, max_new_tokens=float("inf")
    )
    output_text = tokenizer.decode(output[0], skip_special_tokens=True)

    return Outputs(generated_text=output_text[len(prompt) :])
