import cv2
import numpy as np
from hyko_sdk.io import Image
from PIL import Image as PILLImage
from transformers import pipeline

from .metadata import Inputs, Outputs, Params, node


@node.on_startup
async def load(startup_params: Params):
    global detector

    model = startup_params.hugging_face_model
    device_map = startup_params.device_map

    detector = pipeline(
        "object-detection",
        model=model,
        device_map=device_map,
    )


@node.on_call
async def main(inputs: Inputs, params: Params) -> Outputs:
    img = await inputs.input_image.to_pil()
    res = detector(img, threshold=params.threshold)
    image = np.array(img.convert("RGB"))
    for result in res:
        box = result["box"]
        label = result["label"]
        xmin, ymin, xmax, ymax = box["xmin"], box["ymin"], box["xmax"], box["ymax"]
        cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
        cv2.putText(
            image,
            label,
            (xmin, ymin - 5),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 0),
            2,
        )
    final_img = PILLImage.fromarray(image)
    final = await Image.from_pil(final_img)
    return Outputs(final=final)
