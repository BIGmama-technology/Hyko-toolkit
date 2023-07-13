import fastapi
from config import Inputs, Params, Outputs
import torch
from transformers import AutoTokenizer
import transformers

device : torch.device 

if torch.cuda.is_available():
    device = torch.device("cuda:0")
else:
    device = torch.device("cpu")

app = fastapi.FastAPI()

model = "tiiuae/falcon-7b-instruct"
tokenizer = AutoTokenizer.from_pretrained(model)

pipeline = transformers.pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    torch_dtype=torch.bfloat16,
    trust_remote_code=True,
    device_map='auto'
)

@app.post("/", response_model=Outputs)
async def main(inputs: Inputs, params: Params):
    if params.system_prompt:
        prompt = params.system_prompt + "\n" + inputs.prompt
    else:    
        prompt = inputs.prompt
    
    sequences = pipeline(prompt,
            max_length=params.max_length,
            do_sample=True,
            top_k=params.top_k,
            num_return_sequences=params.num_return_sequences,
            eos_token_id=tokenizer.eos_token_id,
        )
    output_text = sequences[0]['generated_text']
    return Outputs(generated_text=output_text)