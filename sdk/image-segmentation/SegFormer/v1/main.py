import numpy as np
import torch
from fastapi.exceptions import HTTPException
from pydantic import Field
from transformers import AutoImageProcessor, SegformerModel

from hyko_sdk.function import SDKFunction
from hyko_sdk.io import Image
from hyko_sdk.metadata import CoreModel

func = SDKFunction(
    description="Image Segmentation Model, this models takes an image and partition it to locate objects and their contours in the image",
    requires_gpu=False,
)


class Inputs(CoreModel):
    image: Image = Field(..., description="User inputted image to be segmented")


class Params(CoreModel):
    pass


class Outputs(CoreModel):
    segmented_image: Image = Field(..., description="Segmented image")


model = None
image_processor = None
device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")


@func.on_startup
async def load():
    global model
    global image_processor
    if model is not None and image_processor is not None:
        print("Model loaded already")
        return

    image_processor = AutoImageProcessor.from_pretrained("nvidia/mit-b0")
    model = SegformerModel.from_pretrained("nvidia/mit-b0").to(device)  # type: ignore


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    if model is None or image_processor is None:
        raise HTTPException(status_code=500, detail="Model is not loaded yet")

    img = inputs.image.to_ndarray()

    img = image_processor(img)
    with torch.no_grad():
        outputs = model(torch.FloatTensor(img.pixel_values[0])[None, :].cuda())

    array = outputs.last_hidden_state.cpu().numpy()
    array = np.swapaxes(array.squeeze()[0:3], 0, -1)
    array = array / array.max()
    array = 255 * array
    array = array.astype(np.uint8)
    segmented_image = Image.from_ndarray(array)

    return Outputs(segmented_image=segmented_image)
