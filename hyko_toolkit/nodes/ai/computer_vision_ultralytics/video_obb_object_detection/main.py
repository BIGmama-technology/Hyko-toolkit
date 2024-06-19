import os
import tempfile

import cv2
import supervision as sv
from fastapi import HTTPException
from hyko_sdk.components.components import Ext
from hyko_sdk.io import Video
from ultralytics import YOLO

from .metadata import Inputs, Outputs, Params, node


@node.on_startup
async def load(startup_params: Params):
    global model, device_map
    device_map = startup_params.device_map
    model = YOLO(f"{startup_params.model.name}-obb.pt")
    if device_map == "auto":
        raise HTTPException(
            status_code=500, detail="AUTO not available as device_map in this Tool."
        )


@node.on_call
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
    # Create an oriented bounding box annotator and LabelAnnotator objects
    oriented_box_annotator = sv.OrientedBoxAnnotator(
        color=sv.ColorPalette.ROBOFLOW, thickness=5
    )
    label_annotator = sv.LabelAnnotator()

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
            iou=params.iou_threshold,
            device=device_map,
        )
        # Convert the results to the supervision Vision format
        detections = sv.Detections.from_ultralytics(results[0])
        labels = [model.model.names[class_id] for class_id in detections.class_id]
        annotated_frame = oriented_box_annotator.annotate(
            scene=frame, detections=detections
        )
        annotated_image = label_annotator.annotate(
            scene=annotated_frame, detections=detections, labels=labels
        )
        out.write(annotated_image)
    # Release the input and output video file resources
    cap.release()
    out.release()
    with open(out_temp_file_path, "rb") as file:
        video_buffer = file.read()
    # Remove the temporary files
    os.unlink(out_temp_file_path)
    os.unlink(input_temp_file_path)
    return Outputs(video=await Video(obj_ext=Ext.MP4).init_from_val(val=video_buffer))
