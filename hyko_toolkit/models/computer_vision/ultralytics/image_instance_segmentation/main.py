import math

import cv2
import cvzone
import numpy as np
from fastapi import HTTPException
from hyko_sdk.io import Image
from metadata import Inputs, Outputs, Params, func
from ultralytics import YOLO


@func.on_startup
async def load(startup_params: Params):
    global model, device_map
    device_map = startup_params.device_map
    model = YOLO(f"{startup_params.model.name}-seg.pt")
    if device_map == "auto":
        raise HTTPException(
            status_code=500, detail="AUTO not available as device_map in this Tool."
        )


@func.on_call
async def main(inputs: Inputs, params: Params) -> Outputs:
    img = await inputs.input_image.to_ndarray()
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    # Use the model to predict the objects in the image
    res = model.predict(source=img, conf=params.threshold, device=device_map)
    # Get the masks and the original image from the prediction results
    masks = res[0].masks
    orig_img = res[0].orig_img
    overlay = np.zeros_like(orig_img)
    for mask_index, box in enumerate(res[0].boxes):
        # Get the xy coordinates of the current mask
        selected_mask_xy = masks.xy[mask_index]
        # Create a blank mask with the same dimensions as the original image
        selected_mask = np.zeros(orig_img.shape[:2], dtype=np.uint8)
        # Fill the current mask with the xy coordinates
        cv2.fillPoly(
            selected_mask, [np.array(selected_mask_xy).astype(np.int32)], color=255
        )
        # Color the overlay image where the mask is not zero
        overlay[selected_mask != 0] = (0, 255, 0)
        # Get the class index of the current box
        clsi = list(res[0].boxes.cls)
        # Get the name of the object from the class index
        object_name = res[0].names[int(clsi[mask_index])]
        # Get the coordinates of the bounding box
        x1, y1, x2, y2 = box.xyxy[0]
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        clsi = int(box.cls[0])
        conf = math.ceil(box.conf[0] * 100) / 100
        w, h = int(x2 - x1), int(y2 - y1)
        # Draw the name of the object and the confidence score on the image
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
    # Blend the original image with the overlay image to highlight the detected objects
    masked_image = cv2.addWeighted(orig_img, 0.7, overlay, 0.3, 0)
    return Outputs(image=await Image.from_ndarray(masked_image[:, :, ::-1]))
