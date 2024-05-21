import os
import tempfile

import cv2
from hyko_sdk.io import Video
from metadata import Inputs, Outputs, Params, func


def convert_video(buffer, codec):
    """
    Convert a video from one format to another.

    Parameters:
        buffer (bytes): The video data in bytes format.
        codec (str): The four-character code for the codec.
    Returns:
        bytes: The converted video data.
    """
    # create a temporary file
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(buffer)
        temp_file_path = temp_file.name

    cap = cv2.VideoCapture(temp_file_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*codec)

    # OpenCV requires dimensions in (width, height) format
    out = cv2.VideoWriter(temp_file_path, fourcc, fps, (width, height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)

    cap.release()
    out.release()

    # Read the converted video data from the temporary file
    with open(temp_file_path, "rb") as file:
        video_buffer = file.read()

    # Remove the temporary file
    os.unlink(temp_file_path)
    return video_buffer


@func.on_call
async def main(inputs: Inputs, params: Params) -> Outputs:
    if params.target_type.name == "webm":
        video_buffer = convert_video(await inputs.input_video.get_data(), codec="VP90")
    else:
        video_buffer = convert_video(await inputs.input_video.get_data(), codec="mp4v")
    return Outputs(
        output_video=await Video(
            obj_ext=params.target_type.value,
        ).init_from_val(
            val=video_buffer,
        )
    )
