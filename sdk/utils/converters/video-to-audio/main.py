
import fastapi
from fastapi.exceptions import HTTPException
from config import Inputs, Params, Outputs, Audio
import base64
import os
import subprocess
app = fastapi.FastAPI()

@app.post("/load", response_model=None)
def load():
    pass

@app.post("/", response_model=Outputs)
async def main(inputs: Inputs, params: Params):
    
    await inputs.video.wait_data()
    if inputs.video.data is None:
        raise HTTPException(
            status_code=500,
            detail="No video data in input video"
        )
        
    with open(f"/app/{inputs.video.filename}", "wb") as f:
        f.write(inputs.video.data)

    subprocess.run(f"ffmpeg -i /app/{inputs.video.filename} /app/audio.mp3 -y".split(" "))

    with open("audio.mp3", "rb") as f:
        data = f.read()
    audio = Audio(bytearray(data), filename="audio.mp3", mime_type="audio/mp3")
    await audio.wait_data()
    return Outputs(audio=audio)


##############################################################################################################

