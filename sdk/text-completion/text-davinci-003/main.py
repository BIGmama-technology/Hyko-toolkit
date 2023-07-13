import fastapi
from config import Inputs, Params, Outputs
import openai

app = fastapi.FastAPI()

#################################################################

# Insert the main code of the function here #################################################################


# keep the decorator, function declaration and return type the same.
# the main function should always take Inputs as the first argument and Params as the second argument.
# should always return Outputs.
@app.post("/", response_model=Outputs)
async def main(inputs: Inputs, params: Params):
    if params.system_prompt:
        prompt = params.system_prompt + "\n" + inputs.prompt
    else:    
        prompt = inputs.prompt
    res = await openai.Completion.acreate(
        model="text-davinci-003",
        prompt=inputs.prompt,
        api_key=params.api_key,
        max_tokens=params.max_tokens,
        temperature=params.temperature,
        top_p=params.top_p,
    )

    return Outputs(generated_text=res.get("choices")[0]["text"]) # type: ignore


##############################################################################################################

