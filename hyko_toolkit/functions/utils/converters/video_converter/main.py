import os

import cv2
from metadata import Inputs, Outputs, Params, func

from hyko_sdk.io import Video
from hyko_sdk.types import Ext


def convert_video(input_file, output_file, codec):
    """
    Convert a video from one format to another.

    Parameters:
        input_file (str): Path to the input video file.
        output_file (str): Path to the output video file.
        codec (str).
    """
    cap = cv2.VideoCapture(input_file)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*codec)
    out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)
    cap.release()
    out.release()


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    _, ext = os.path.splitext(inputs.input_video.get_name())
    type_to_object = {
        "webm": Ext.WEBM,
        "mp4": Ext.MP4,
        "avi": Ext.AVI,
        "mkv": Ext.MKV,
        "mov": Ext.MOV,
        "wmv": Ext.WMV,
    }

    with open(f"/app/video{ext}", "wb") as f:
        f.write(inputs.input_video.get_data())

    output_file = f"/app/result_video.{params.target_type.value}"

    if params.target_type == "webm":
        convert_video(f"/app/video{ext}", output_file, codec="VP90")
    else:
        convert_video(f"/app/video{ext}", output_file, codec="mp4v")

    with open(output_file, "rb") as f:
        data = f.read()
    return Outputs(
        output_video=Video(val=data, obj_ext=type_to_object[params.target_type])
    )
