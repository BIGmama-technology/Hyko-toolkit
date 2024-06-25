import cv2
from fastapi import HTTPException
from ultralytics import YOLO

from .metadata import Inputs, Outputs, Params, node


@node.on_startup
async def load(startup_params: Params):
    global model, device_map
    device_map = startup_params.device_map
    model = YOLO(f"{startup_params.model.name}-cls.pt")
    if device_map == "auto":
        raise HTTPException(
            status_code=500, detail="AUTO not available as device_map in this Tool."
        )


@node.on_call
async def main(inputs: Inputs, params: Params) -> Outputs:
    img = await inputs.input_image.to_ndarray()
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    # predict on an image
    results = model.predict(source=img, conf=params.threshold, device=device_map)

    # Get the names of the classes from the results
    names = results[0].names

    # Get the top 5 confidence scores for the prediction
    top5conf = results[0].probs.top5conf
    top5conf_list = [tensor.item() for tensor in top5conf]

    # Get the top 5 class indices from the results
    top5_cli = results[0].probs.top5

    # Get the names of the top 5 classes
    class_names = [names[i] for i in top5_cli]

    return Outputs(top5_class_names=class_names, top5_conf=top5conf_list)
