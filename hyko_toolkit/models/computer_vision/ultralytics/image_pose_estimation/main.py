import math

import cv2
import cvzone
from fastapi import HTTPException
from hyko_sdk.components import Ext
from hyko_sdk.io import Image
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
    image = await inputs.input_image.to_ndarray()
    # Convert the input image from RGB to BGR format
    img = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    # predict the objects in the image
    results = model.predict(
        source=img, conf=params.threshold, iou=params.iou_threshold, device=device_map
    )
    # get class names, boxes , keypoints
    names = results[0].names
    boxes = results[0].boxes
    clsi = list(results[0].boxes.cls)
    keypoints = results[0].keypoints
    keypoints_tensor = keypoints.xy
    # Move the tensor to CPU and convert it to a NumPy array
    keypoints_array = keypoints_tensor.cpu().numpy()
    # Iterate over the people in the image
    for keypoint in keypoints_array:
        # Iterate over the keypoints of the object and draw circles
        for kpt in keypoint:
            # convert x and y to integers
            x, y = map(int, kpt)
            # skip keypoints with (0, 0) coordinatess
            if x != 0 and y != 0:
                cv2.circle(img, (x, y), radius=3, color=(0, 255, 0), thickness=-1)
    for box in boxes:
        x1, y1, x2, y2 = box.xyxy[0]
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        clsi = int(box.cls[0])
        conf = math.ceil(box.conf[0] * 100) / 100
        w, h = int(x2 - x1), int(y2 - y1)
        # Draw bounding box and label on the frame
        cvzone.cornerRect(img, (x1, y1, w, h), l=3, rt=1)
        cvzone.putTextRect(
            img,
            f"{names[clsi]} {conf}",
            (max(0, x1), max(20, y1)),
            thickness=1,
            colorR=(0, 0, 255),
            scale=0.9,
            offset=3,
        )
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return Outputs(image=await Image.from_ndarray(img, encoding=Ext.PNG))
