from fastapi import FastAPI
from config import Inputs, Params, Outputs
import openai

app = FastAPI()

@app.post(
    "/load",
    response_model=None,
)
def load():
    pass

@app.post(
    "/",
    response_model=Outputs,
)
async def main(inputs: Inputs, params: Params):

    res = await openai.Completion.acreate(
        model="text-davinci-003",
        prompt="Summarize this: \n" + inputs.text,
        api_key=params.api_key,
        max_tokens=params.max_tokens,
        temperature=params.temperature,
        top_p=params.top_p,
    )

    return Outputs(summary=res.get("choices")[0]["text"]) # type: ignore
