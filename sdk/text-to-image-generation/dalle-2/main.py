import fastapi
from .config import Inputs, Params, Outputs
import openai

app = fastapi.FastAPI()

#################################################################

# Insert the main code of the function here #################################################################


# keep the decorator, function declaration and return type the same.
# the main function should always take Inputs as the first argument and Params as the second argument.
# should always return Outputs.
@app.post("/", response_model=Outputs)
async def main(inputs: Inputs, params: Params):

    res = await openai.Image.acreate(
        prompt=inputs.prompt,
        api_key=params.api_key,
        response_format="b64_json",
        n=1,
        size="256x256",
    )

    img_encoded = "data:image/png;base64," + res.get("data")[0]["b64_json"] # type: ignore

    return Outputs(generated_image=img_encoded)



##############################################################################################################

