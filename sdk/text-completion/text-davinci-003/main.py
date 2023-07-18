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
        prompt = f"{inputs.prompt}"
    else:    
        prompt = params.system_prompt + '\n' + inputs.prompt

    # print(f"prompt: {prompt}")

    print(f"inputs: {inputs}")
    print(f"params: {params}")

    res = await openai.Completion.acreate(
        model="text-davinci-003",
        prompt=prompt,
        api_key=f"{params.api_key}",
        max_tokens=params.max_tokens,
        temperature=params.temperature,
        top_p=params.top_p,
    )

    print(f"res: {res}")

    completion: str = res.get("choices")[0]["text"] # type: ignore

    print(f"completion: {completion}")

    return Outputs(completion_text=completion)


##############################################################################################################

