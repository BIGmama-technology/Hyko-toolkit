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

    if params.system_prompt is None:
        messages=[
            {
                "role": "user",
                "content": inputs.prompt
            },
        ]
    else:
        messages=[
            {
                "role": "system",
                "content": params.system_prompt,
            },
            {
                "role": "user",
                "content": inputs.prompt
            },
        ]

    chat_completion = await openai.ChatCompletion.acreate(
        model="gpt-4-32k-0613",
        messages=messages,
        api_key=params.api_key,
        max_tokens=params.max_tokens,
        temperature=params.temperature,
        top_p=params.top_p,
    )

    completion: str = chat_completion.choices[0].message.content # type: ignore

    return Outputs(completion_text=completion)


##############################################################################################################

