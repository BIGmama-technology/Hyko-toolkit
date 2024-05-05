import math
import os
import tempfile

import cv2
import cvzone
from fastapi import HTTPException
from hyko_sdk.components import Ext
from hyko_sdk.io import Video
from metadata import Inputs, Outputs, Params, StartupParams, func
from ultralytics import YOLO


@func.on_startup
async def load(startup_params: StartupParams):
    global model, device_map
    device_map = startup_params.device_map
    if startup_params.model.name == "yolov8x_p6":
        model = YOLO("yolov8x-pose-p6.pt")
    else:
        model = YOLO(f"{startup_params.model.name}-pose.pt")
    if device_map == "auto":
        raise HTTPException(
            status_code=500, detail="AUTO not available as device_map in this Tool."
        )


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    # Create a TEMP file to store the input video data
    with tempfile.NamedTemporaryFile(delete=False) as input_v:
        input_v.write(await inputs.input_video.get_data())
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
            source=frame,
            conf=params.threshold,
            device=device_map,
        )
        boxes = results[0].boxes
        names = results[0].names
        keypoints = results[0].keypoints
        keypoints_tensor = keypoints.xy
        # Move the tensor to CPU and convert it to a NumPy array
        keypoints_array = keypoints_tensor.cpu().numpy()
        # Iterate over the people in the image
        for keypoint in keypoints_array:
            # Iterate over the keypoints of the person and draw circles
            for kpt in keypoint:
                x, y = map(int, kpt)  # convert x and y to integers
                if x != 0 and y != 0:  # skip keypoints with (0, 0) coordinates
                    cv2.circle(frame, (x, y), radius=3, color=(0, 255, 0), thickness=-1)
        for box in boxes:
            clsi = list(results[0].boxes.cls)
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
    return Outputs(video=await Video(obj_ext=Ext.MP4).init_from_val(video_buffer))
