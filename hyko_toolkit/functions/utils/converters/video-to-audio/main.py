import os
import subprocess

from metadata import Inputs, Outputs, Params, func

from hyko_sdk.io import Audio


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    _, ext = os.path.splitext(inputs.video.get_name())

    with open(f"/app/video.{ext}", "wb") as f:
        f.write(inputs.video.get_data())
    # user video.{ext} instead of filename directly to avoid errors with names that has space in it
    subprocess.run(f"ffmpeg -i /app/video.{ext} -ac 1 /app/audio.mp3 -y".split(" "))

    with open("audio.mp3", "rb") as f:
        data = f.read()

    audio = Audio(bytearray(data), filename="audio.mp3", mime_type="MPEG")
    os.remove("audio.mp3")
    return Outputs(audio=audio)
