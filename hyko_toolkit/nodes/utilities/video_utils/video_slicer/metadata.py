import os
import subprocess
import tempfile

from hyko_sdk.components.components import Ext
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.io import Video
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.exceptions import VideoSlicingError

node = ToolkitNode(
    name="Video Slicer",
    cost=0,
    description="Slice a video from any to any time",
    icon="video",
)


@node.set_input
class Inputs(CoreModel):
    video: Video = field(description="Input video to slice")
    timestamps: str = field(description="Start and end time to slice the video")


@node.set_param
class Params(CoreModel):
    pass


@node.set_output
class Outputs(CoreModel):
    sliced_video: Video = field(
        description="The sliced video result",
    )


@node.on_call
async def call(inputs: Inputs, params: Params) -> Outputs:
    start_time, end_time = (time.strip() for time in inputs.timestamps.split("-"))

    temp_input_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    temp_output_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")

    temp_input_file.write(await inputs.video.get_data())
    temp_input_file.flush()

    with open(temp_input_file.name, "wb") as file:
        file.write(await inputs.video.get_data())

    # Construct the FFmpeg command
    command = [
        "ffmpeg",
        "-i",
        temp_input_file.name,
        "-ss",
        start_time,
        "-to",
        end_time,
        "-c:v",
        "libx264",
        "-c:a",
        "aac",
        temp_output_file.name,
        "-y",
    ]

    try:
        subprocess.run(command, check=True, capture_output=True)

        output_binary = None
        with open(temp_output_file.name, "rb") as f:
            output_binary = f.read()

        video = await Video(obj_ext=Ext.MP4).init_from_val(val=output_binary)

        os.unlink(temp_input_file.name)
        os.unlink(temp_output_file.name)

        return Outputs(sliced_video=video)

    except subprocess.CalledProcessError as e:
        raise VideoSlicingError from e
