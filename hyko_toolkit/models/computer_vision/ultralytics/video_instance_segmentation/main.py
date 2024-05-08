import math
import os
import tempfile

import cv2
import cvzone
import numpy as np
from fastapi import HTTPException
from hyko_sdk.components.components import Ext
from hyko_sdk.io import Video
from metadata import Inputs, Outputs, Params, StartupParams, func
from ultralytics import YOLO


@func.on_startup
async def load(startup_params: StartupParams):
    global model, device_map
    device_map = startup_params.device_map
    model = YOLO(f"{startup_params.model.name}-seg.pt")
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
    # Open the input video file
    cap = cv2.VideoCapture(input_temp_file_path)
    # Get the video's frame width, frame height, and frames per second (fps)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    # Create the cv2.VideoWriter object to write the output video
    out = cv2.VideoWriter(
        out_temp_file_path,
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps,
        (frame_width, frame_height),
    )
    # Process the video frame by frame
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        # Perform object detection, masking, and bounding box drawing
        res = model.predict(source=frame, conf=params.threshold, device=device_map)
        masks = res[0].masks
        boxes = res[0].boxes
        orig_img = res[0].orig_img
        overlay = np.zeros_like(orig_img)

        # Iterate through each detected object (box) and its corresponding mask
        for mask_index, box in enumerate(boxes):
            # Get the mask's polygon coordinates
            selected_mask_xy = masks.xy[mask_index]

            # Create an empty mask with the same dimensions as the original image
            selected_mask = np.zeros(orig_img.shape[:2], dtype=np.uint8)

            # Create an empty mask with the same dimensions as the original image
            cv2.fillPoly(
                selected_mask, [np.array(selected_mask_xy).astype(np.int32)], color=255
            )

            # Apply the green color to the mask overlay where the mask is not equal to 0
            overlay[selected_mask != 0] = (0, 255, 0)

            # Get the class index of the detected object
            clsi = list(res[0].boxes.cls)
            object_name = res[0].names[int(clsi[mask_index])]

            # Get the bounding box coordinates (x1, y1, x2, y2) as integers
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

            # Get the confidence
            conf = math.ceil(box.conf[0] * 100) / 100

            # Calculate the width and height of the bounding box
            w, h = int(x2 - x1), int(y2 - y1)

            # Draw the object name and confidence score above the bounding box
            cvzone.cornerRect(orig_img, (x1, y1, w, h), l=3, rt=1)
            cvzone.putTextRect(
                orig_img,
                f"{object_name} {conf}",
                (max(0, x1), max(20, y1)),
                thickness=1,
                colorR=(0, 0, 255),
                scale=0.9,
                offset=3,
            )

        masked_image = cv2.addWeighted(orig_img, 0.7, overlay, 0.3, 0)
        # Write the processed frame to the output video file
        out.write(masked_image[:, :, ::-1])
    cap.release()
    out.release()

    with open(out_temp_file_path, "rb") as file:
        video_buffer = file.read()

    # Remove the temporary files
    os.unlink(out_temp_file_path)
    os.unlink(input_temp_file_path)
    return Outputs(
        video=await Video(
            obj_ext=Ext.MP4,
        ).init_from_val(
            val=video_buffer,
        )
    )
