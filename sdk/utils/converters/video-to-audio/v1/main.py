import os
import subprocess

from pydantic import Field

from hyko_sdk.function import SDKFunction
from hyko_sdk.io import Audio, Video
from hyko_sdk.metadata import CoreModel

func = SDKFunction(
    description="Convert a video type to audio type (takes only the audio data)",
    requires_gpu=False,
)


class Inputs(CoreModel):
    video: Video = Field(..., description="User input video to be converted to audio")


class Params(CoreModel):
    pass


class Outputs(CoreModel):
    audio: Audio = Field(..., description="converted audio")


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
