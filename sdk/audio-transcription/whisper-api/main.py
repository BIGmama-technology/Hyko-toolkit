import fastapi
from config import Inputs, Params, Outputs
import openai
import base64
import io

app = fastapi.FastAPI()

#################################################################

# Insert the main code of the function here #################################################################


# keep the decorator, function declaration and return type the same.
# the main function should always take Inputs as the first argument and Params as the second argument.
# should always return Outputs.
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
        language=inputs.language,
        temperature=params.temperature,
    )

    return Outputs(transcript=res.get("text")) # type: ignore



##############################################################################################################

