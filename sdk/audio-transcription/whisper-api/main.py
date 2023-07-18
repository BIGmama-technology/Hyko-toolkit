import fastapi
from config import Inputs, Params, Outputs
import openai
import base64
import io

app = fastapi.FastAPI()

@app.post("/load", response_model=None)
def load():
   pass

@app.post("/", response_model=Outputs)
async def main(inputs: Inputs, params: Params):

    meta, data = inputs.audio.split(',', 1)

    file = io.BytesIO(base64.urlsafe_b64decode(data))
    file.name = "audio.webm"

    res = await openai.Audio.atranscribe(
        model="whisper-1",
        file=file,
        api_key=params.api_key,
        prompt= inputs.prompt,
        language=params.language,
        temperature=params.temperature,
    )

    return Outputs(transcript=res.get("text")) # type: ignore
