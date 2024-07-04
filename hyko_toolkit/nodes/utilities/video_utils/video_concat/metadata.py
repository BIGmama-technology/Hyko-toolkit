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
    name="Video Concatenator",
    cost=0,
    description="Concatenate three video parts with dynamic fade transitions",
    icon="video",
)


@node.set_input
class Inputs(CoreModel):
    video1: Video = field(description="First video part")
    video2: Video = field(description="Second video part")
    video3: Video = field(description="Third video part")


@node.set_param
class Params(CoreModel):
    pass


@node.set_output
class Outputs(CoreModel):
    concatenated_video: Video = field(
        description="The concatenated video result with transitions",
    )


@node.on_call
async def call(inputs: Inputs, params: Params) -> Outputs:
    def get_duration(file_path: str):
        result = subprocess.run(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                file_path,
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        return float(result.stdout)

    temp_input_file1 = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    temp_input_file2 = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    temp_input_file3 = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    temp_output_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")

    temp_input_file1.write(await inputs.video1.get_data())
    temp_input_file1.flush()
    temp_input_file2.write(await inputs.video2.get_data())
    temp_input_file2.flush()
    temp_input_file3.write(await inputs.video3.get_data())
    temp_input_file3.flush()

    with open(temp_input_file1.name, "wb") as file:
        file.write(await inputs.video1.get_data())

    with open(temp_input_file2.name, "wb") as file:
        file.write(await inputs.video2.get_data())

    with open(temp_input_file3.name, "wb") as file:
        file.write(await inputs.video3.get_data())

    # Calculate durations and fade durations
    durations = [
        get_duration(temp_input_file1.name),
        get_duration(temp_input_file2.name),
        get_duration(temp_input_file3.name),
    ]

    # Construct the filter_complex part
    filter_complex = f"""
    [0:v]trim=start=0:end={durations[0]},fade=t=out:st={durations[0] - 0.3}:d={0.3}[v0];
    [1:v]trim=start=0:end={durations[1]},fade=t=in:st=0:d={0.3},fade=t=out:st={durations[1] - 0.3}:d={0.3}[v1];
    [2:v]trim=start=0:end={durations[2]},fade=t=in:st=0:d={0.3}[v2];
    [v0][0:a][v1][1:a][v2][2:a]concat=n=3:v=1:a=1[outv][outa]
    """

    # Construct the FFmpeg command
    command = [
        "ffmpeg",
        "-i",
        temp_input_file1.name,
        "-i",
        temp_input_file2.name,
        "-i",
        temp_input_file3.name,
        "-filter_complex",
        filter_complex,
        "-map",
        "[outv]",
        "-map",
        "[outa]",
        "-c:v",
        "libx264",
        "-c:a",
        "aac",
        "-vsync",
        "2",
        temp_output_file.name,
        "-y",
    ]

    try:
        subprocess.run(command, check=True, capture_output=True)

        output_binary = None
        with open(temp_output_file.name, "rb") as f:
            output_binary = f.read()

        video = await Video(obj_ext=Ext.MP4).init_from_val(val=output_binary)

        os.unlink(temp_input_file1.name)
        os.unlink(temp_input_file2.name)
        os.unlink(temp_input_file3.name)
        os.unlink(temp_output_file.name)

        return Outputs(concatenated_video=video)

    except subprocess.CalledProcessError as e:
        raise VideoSlicingError from e
