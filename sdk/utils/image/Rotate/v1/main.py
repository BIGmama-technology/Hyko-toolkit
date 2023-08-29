from pydantic import Field
from hyko_sdk import CoreModel, Image, SDKFunction
import numpy as np
import os
import cv2
from PIL import Image as PIL_Image

func = SDKFunction(
    description="Rotate an image by a given angle",
    requires_gpu=False,
)

class Inputs(CoreModel):
    image: Image = Field(..., description="Input image to be rotated")

class Params(CoreModel):
    rotation_angle: int = Field(..., description="Rotation angle in degrees")

class Outputs(CoreModel):
    rotated_image: Image = Field(..., description="Rotated image")


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    _, ext = os.path.splitext(inputs.image.get_name())

    with open(f"./image{ext}", "wb") as f:
        f.write(inputs.image.get_data())

    image = PIL_Image.open(f"./image{ext}")
    image_cv2 = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    height, width, _ = image_cv2.shape
    
    rotation_matrix = cv2.getRotationMatrix2D((width/2, height/2), params.rotation_angle, 1)
    rotated_image = cv2.warpAffine(image_cv2, rotation_matrix, (width, height))
    rotated_rgb_image = cv2.cvtColor(rotated_image, cv2.COLOR_BGR2RGB)
   

    image = Image.from_ndarray(rotated_rgb_image)
   
    return Outputs(rotated_image=image)

