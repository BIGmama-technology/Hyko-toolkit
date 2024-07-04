import logging
import os
import subprocess
import tempfile

from hyko_sdk.components.components import Ext
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.io import Video
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.exceptions import VideoSubtitleWritingError

node = ToolkitNode(
    name="Subtitle writer",
    cost=0,
    description="Add Subtitles to a video",
    icon="video",
)


@node.set_input
class Inputs(CoreModel):
    video: Video = field(description="Input video to add subtitles")
    subtitles_string: str = field(
        description="The subtitles string in srt format",
    )


@node.set_param
class Params(CoreModel):
    pass


@node.set_output
class Outputs(CoreModel):
    output_video: Video = field(
        description="The resulted video with subtitles",
    )


@node.on_call
async def call(inputs: Inputs, params: Params) -> Outputs:
    temp_input_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    temp_output_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    temp_subtitles_file = tempfile.NamedTemporaryFile(delete=False, suffix=".srt")

    temp_input_file.write(await inputs.video.get_data())
    temp_input_file.flush()

    with open(temp_subtitles_file.name, "w") as file:
        file.write(inputs.subtitles_string)

    with open(temp_input_file.name, "wb") as file:
        file.write(await inputs.video.get_data())

    command = [
        "ffmpeg",
        "-i",
        temp_input_file.name,
        "-vf",
        f"subtitles={temp_subtitles_file.name}:force_style='FontName=Open Sans,FontSize=16,PrimaryColour=&HFFFFFF&,OutlineColour=&H000000&,Outline=1,Shadow=1'",
        temp_output_file.name,
        "-y",
    ]
    try:
        subprocess.run(command, check=True)

        output_binary = None
        with open(temp_output_file.name, "rb") as f:
            output_binary = f.read()

        video = await Video(obj_ext=Ext.MP4).init_from_val(val=output_binary)

        os.unlink(temp_input_file.name)
        os.unlink(temp_output_file.name)
        os.unlink(temp_subtitles_file.name)

        return Outputs(output_video=video)

    except subprocess.CalledProcessError as e:
        logging.warning(e)
        raise VideoSubtitleWritingError from e
