import fastapi
from config import Inputs, Params, Outputs
import openai

app = fastapi.FastAPI()
@app.post("/load", response_model=None)
def load():
    pass

@app.post("/", response_model=Outputs)
async def main(inputs: Inputs, params: Params):
    if params.system_prompt:
        prompt = params.system_prompt + "\n" + inputs.prompt
    else:    
        prompt = inputs.prompt
    res = await openai.Completion.acreate(
        model="text-davinci-003",
        prompt=prompt,
        api_key=params.api_key,
        max_tokens=params.max_tokens,
        temperature=params.temperature,
        top_p=params.top_p,
    )

    return Outputs(generated_text=res.get("choices")[0]["text"]) # type: ignore


##############################################################################################################

