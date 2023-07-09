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
    device_map="auto",
)

@app.post("/", response_model=Outputs)
async def main(inputs: Inputs, params: Params):
    if params.pre_prompt:
        prompt = params.pre_prompt + "\n" + inputs.input_prompt
    else:    
        prompt = inputs.input_prompt
    
    sequences = pipeline(prompt,
            max_length=200,
            do_sample=True,
            top_k=10,
            num_return_sequences=1,
            eos_token_id=tokenizer.eos_token_id,
        )
    output_text = sequences[0]['generated_text']
    return Outputs(generated_text=output_text)