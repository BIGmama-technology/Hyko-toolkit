import io

from hyko_sdk.components import Ext
from hyko_sdk.io import Video
from metadata import (
    Inputs,
    Outputs,
    Params,
    func,
)
from pytube import YouTube


def download_video(url, resolution):
    """
    Download a video from YouTube.

    Args:
    - url (str): The URL of the YouTube video to download.
    - resolution (str): The desired resolution of the video. Options: 'highest', 'lowest', or specific resolution like '720p', '360p', etc. Default is 'highest'.

    Returns:
    - bytes: The video content as bytes if successful, otherwise None.
    """

    yt = YouTube(url)
    if resolution == "highest":
        stream = yt.streams.get_highest_resolution()
    elif resolution == "lowest":
        stream = yt.streams.get_lowest_resolution()
    else:
        stream = yt.streams.filter(res=resolution).first()
    # Download video to memory buffer
    video_buffer = io.BytesIO()
    stream.stream_to_buffer(video_buffer)
    video_content = video_buffer.getvalue()
    video_buffer.close()
    return video_content


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    data = download_video(url=inputs.video_url, resolution=params.resolution.value)
    return Outputs(output_video=await Video(obj_ext=Ext.MP4).init_from_val(data))
