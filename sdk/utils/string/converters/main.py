
import fastapi
from fastapi.exceptions import HTTPException
from config import Inputs, Params, Outputs
from hyko_sdk import error, io
import base64
import os
import subprocess
app = fastapi.FastAPI()

#################################################################

# Insert the main code of the function here #################################################################


# keep the decorator, function declaration and return type the same.
# the main function should always take Inputs as the first argument and Params as the second argument.
# should always return Outputs.
@app.post("/", response_model=Outputs)
async def main(inputs: Inputs, params: Params):
    if len(inputs.video.split(",")) != 2:
        raise HTTPException(status_code=500, detail=error.Errors.InvalidBase64)    
    header, data = inputs.video.split(",")
    if not ("video" in header) and not ("webm" in header):
        raise HTTPException(status_code=500, detail=error.Errors.InvalidBase64)  
    base64_bytes = base64.b64decode(data)

    if os.path.exists("video.webm"):
        os.remove("video.webm")
    with open("video.webm", "wb") as f:
        f.write(base64_bytes)
    if os.path.exists("audio.webm"):
        os.remove("audio.webm")

    if os.path.exists("audio.wav"):
        os.remove("audio.wav")
    subprocess.run("ffmpeg -i video.webm audio.wav")
    subprocess.run("ffmpeg -i audio.wav audio.webm")

    with open("audio.webm", "rb") as f:
        data = f.read()

    audio = "data:video/webm;base64" + data.decode()
    return Outputs(audio=io.Audio(audio))


##############################################################################################################

