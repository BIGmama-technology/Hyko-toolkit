import math
import os
import tempfile

import cv2
import cvzone
from metadata import Inputs, Outputs, Params, StartupParams, func
from ultralytics import YOLO

from hyko_sdk.io import Video
from hyko_sdk.models import Ext


@func.on_startup
async def load(startup_params: StartupParams):
    global model
    model = YOLO(f"{startup_params.model.name}.pt")


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    # Create a TEMP file to store the input video data
    with tempfile.NamedTemporaryFile(delete=False) as input_v:
        input_v.write(inputs.input_video.get_data())
        input_temp_file_path = input_v.name
    # Create a TEMP file to store the output video data with an 'mp4 suffix'
    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as out_v:
        out_temp_file_path = out_v.name

    cap = cv2.VideoCapture(input_temp_file_path)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    # Create a VideoWriter object to write the output video file
    out = cv2.VideoWriter(
        out_temp_file_path,
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps,
        (frame_width, frame_height),
    )
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        # Use the model to predict the objects in the current frame
        results = model.predict(
            source=frame, conf=params.threshold, iou=params.iou_threshold
        )
        bboxs = results[0].boxes
        names = results[0].names
        for box in bboxs:
            # Extract bounding box coordinates
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            clsi = int(box.cls[0])
            conf = math.ceil(box.conf[0] * 100) / 100
            w, h = int(x2 - x1), int(y2 - y1)

            # Draw bounding box and label on the frame
            cvzone.cornerRect(frame, (x1, y1, w, h), l=3, rt=1)
            cvzone.putTextRect(
                frame,
                f"{names[clsi]} {conf}",
                (max(0, x1), max(20, y1)),
                thickness=1,
                colorR=(0, 0, 255),
                scale=0.9,
                offset=3,
            )
        # Write the frame to the output video file
        out.write(frame)
    # Release the input and output video file resources
    cap.release()
    out.release()
    with open(out_temp_file_path, "rb") as file:
        video_buffer = file.read()
    # Remove the temporary files
    os.unlink(out_temp_file_path)
    os.unlink(input_temp_file_path)
    return Outputs(video=Video(val=video_buffer, obj_ext=Ext.MP4))
