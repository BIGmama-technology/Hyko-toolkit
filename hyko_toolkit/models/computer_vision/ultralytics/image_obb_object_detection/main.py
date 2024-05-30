import cv2
import supervision as sv
from fastapi import HTTPException
from hyko_sdk.components.components import Ext
from hyko_sdk.io import Image
from ultralytics import YOLO

from .metadata import Inputs, Outputs, Params, func


@func.on_startup
async def load(startup_params: Params):
    global model, device_map
    device_map = startup_params.device_map
    model = YOLO(f"{startup_params.model.name}-obb.pt")
    if device_map == "auto":
        raise HTTPException(
            status_code=500, detail="AUTO not available as device_map in this Tool."
        )


@func.on_call
async def main(inputs: Inputs, params: Params) -> Outputs:
    image = await inputs.input_image.to_ndarray()
    # Convert the input image from RGB to BGR format
    img = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    # predict the objects in the image
    results = model.predict(
        source=img, conf=params.threshold, iou=params.iou_threshold, device=device_map
    )
    # Convert the results to the supervision Vision format
    detections = sv.Detections.from_ultralytics(results[0])
    # Create an oriented bounding box annotator and LabelAnnotator objects
    oriented_box_annotator = sv.OrientedBoxAnnotator()
    label_annotator = sv.LabelAnnotator()

    # Get the labels for the detected objects
    labels = [model.model.names[class_id] for class_id in detections.class_id]

    # Annotate the image
    annotated_frame = oriented_box_annotator.annotate(scene=img, detections=detections)
    annotated_image = label_annotator.annotate(
        scene=annotated_frame, detections=detections, labels=labels
    )
    return Outputs(
        image=await Image.from_ndarray(
            cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR),
            encoding=Ext.PNG,
        )
    )
