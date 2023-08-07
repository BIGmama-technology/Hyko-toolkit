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

    chat_completion = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "Summarize this",
            },
            {
                "role": "user",
                "content": inputs.text,
            },
        ],
        api_key=params.api_key,
        max_tokens=params.max_tokens,
        temperature=params.temperature,
        top_p=params.top_p,
    )

    completion: str = chat_completion.choices[0].message.content # type: ignore

    return Outputs(summary=completion)


##############################################################################################################

