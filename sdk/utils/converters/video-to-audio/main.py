
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
    # data:image/png;base64
    try:
        file_format = header.split("/")[1].split(";")[0]
        print(file_format)
    except:
        raise HTTPException(status_code=500, detail=error.Errors.InvalidBase64)  

    # if not ("video" in header) and not ("webm" in header):
    #     raise HTTPException(status_code=500, detail=error.Errors.InvalidBase64)  




    base64_bytes = base64.b64decode(data)

    with open(f"/app/video.{file_format}", "wb") as f:
        f.write(base64_bytes)

    subprocess.run(f"ffmpeg -i /app/video.{file_format} /app/audio.mp3 -y".split(" "))
    subprocess.run("ffmpeg -i /app/audio.mp3 /app/audio.webm -y".split(" "))

    with open("audio.webm", "rb") as f:
        data = f.read()
    data = base64.b64encode(data)
    audio = "data:video/webm;base64," + data.decode()
    return Outputs(audio=io.Audio(audio))


##############################################################################################################

