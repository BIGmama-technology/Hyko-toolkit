import os
import subprocess
import tempfile

from hyko_sdk.components.components import Ext
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.io import Audio, Video
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.exceptions import VideoToAudioConversionError

node = ToolkitNode(
    name="Video to audio",
    cost=3,
    description="Convert a video type to audio type (takes only the audio data)",
    icon="video",
)


@node.set_input
class Inputs(CoreModel):
    video: Video = field(description="User input video to be converted to audio")


@node.set_output
class Outputs(CoreModel):
    audio: Audio = field(description="converted audio")


@node.on_call
async def main(inputs: Inputs, params: CoreModel) -> Outputs:
    temp_input_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    temp_output_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")

    temp_input_file.write(await inputs.video.get_data())
    temp_input_file.flush()

    with open(temp_input_file.name, "wb") as f:
        f.write(await inputs.video.get_data())
    # user video.{ext} instead of filename directly to avoid errors with names that has space in it

    try:
        subprocess.run(
            f"ffmpeg -i {temp_input_file.name} -ac 1 {temp_output_file.name} -y".split(
                " "
            ),
            check=True,
            capture_output=True,
        )

        output_binary = None
        with open(temp_output_file.name, "rb") as f:
            output_binary = f.read()

        audio = await Audio(obj_ext=Ext.MP3).init_from_val(val=output_binary)

        os.unlink(temp_input_file.name)
        os.unlink(temp_output_file.name)

        return Outputs(audio=audio)

    except subprocess.CalledProcessError as e:
        raise VideoToAudioConversionError from e
