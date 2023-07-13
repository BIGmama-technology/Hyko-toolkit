import fastapi
from config import Inputs, Params, Outputs
import openai

app = fastapi.FastAPI()

@app.post("/", response_model=Outputs)
async def main(inputs: Inputs, params: Params):

    res = await openai.Completion.acreate(
        model="text-davinci-003",
        prompt=f"Translate this to {params.language}: \n" + inputs.prompt,
        api_key=params.api_key,
        max_tokens=params.max_tokens,
        temperature=params.temperature,
        top_p=params.top_p,
    )

    return Outputs(translated_text=res.get("choices")[0]["text"]) # type: ignore
