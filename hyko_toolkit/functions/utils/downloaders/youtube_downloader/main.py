import os

from metadata import (
    Inputs,
    Outputs,
    Params,
    func,
)
from pytube import YouTube

from hyko_sdk.io import Video
from hyko_sdk.types import Ext


def download_video(url, output_path, resolution):
    """
    Download a video from YouTube.

    Args:
    - url (str): The URL of the YouTube video to download.
    - output_path (str): The directory where the downloaded video will be saved.
    - resolution (str): The desired resolution of the video. Options: 'highest', 'lowest', or specific resolution like '720p', '360p', etc. Default is 'highest'.

    Returns:
    - str: The file path of the downloaded video if successful, otherwise None.
    """
    try:
        yt = YouTube(url)
        if resolution == "highest":
            stream = yt.streams.get_highest_resolution()
        elif resolution == "lowest":
            stream = yt.streams.get_lowest_resolution()
        else:
            stream = yt.streams.filter(res=resolution).first()
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        file_path = stream.download(output_path)
        return file_path
    except Exception:
        return None


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    downloaded_file_path = download_video(
        inputs.video_url, output_path="results", resolution=params.resolution.value
    )

    with open(downloaded_file_path, "rb") as f:
        data = f.read()
    return Outputs(output_video=Video(val=data, obj_ext=Ext.MP4))
