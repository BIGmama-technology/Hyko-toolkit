import fastapi
from config import Inputs, Params, Outputs, Image
import openai
import base64

app = fastapi.FastAPI()

@app.post("/load", response_model=None)
def load():
    pass

@app.post("/", response_model=Outputs)
async def main(inputs: Inputs, params: Params):

    res = await openai.Image.acreate(
        prompt=inputs.prompt,
        api_key=params.api_key,
        response_format="b64_json",
        n=1,
        size="256x256",
    )

    img = base64.b64decode(res.get("data")[0]["b64_json"])
    img = Image(bytearray(img), filename="iamge.png", mime_type="image/png")
    await img.wait_data()
    return Outputs(generated_image=img)



##############################################################################################################

