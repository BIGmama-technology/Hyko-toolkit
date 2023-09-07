from fastapi import HTTPException
from pydantic import Field
from hyko_sdk import CoreModel, SDKFunction, Image
import os
import cv2
import numpy as np
from PIL import Image as PIL_Image


func = SDKFunction(
    description="Crop an image from the specified edges",
    requires_gpu=False,
)

class Inputs(CoreModel):
    image: Image = Field(..., description="Input image")



class Params(CoreModel):
    top: int = Field(..., description="Number of pixels to crop from the top")
    left: int = Field(..., description="Number of pixels to crop from the left")
    right: int = Field(..., description="Number of pixels to crop from the right")
    bottom: int = Field(..., description="Number of pixels to crop from the bottom")


class Outputs(CoreModel):
    cropped_image: Image = Field(..., description="Output cropped image")


@func.on_execute
async def main(inputs: Inputs , params: Params)-> Outputs:
    
    file, ext = os.path.splitext(inputs.image.get_name())
    with open(f"./image{ext}", "wb") as f:
        f.write(inputs.image.get_data())
    
    image = PIL_Image.open(f"./image{ext}")
    
    image_cv2 = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    height, width, _ = image_cv2.shape
    
     
    if (
    params.top < 0 or
    params.left < 0 or
    params.right < 0 or
    params.bottom < 0 
    ):
     raise HTTPException(
        status_code=500,
        detail="Crop parameters must not be less than 0"
    )

    cropped_image = image_cv2[params.top:height-params.bottom, params.left:width-params.right]
    
    if cropped_image.size == 0:
        raise HTTPException(
            status_code=500,
            detail="Cropped area resulted in an empty image"
    )

    cropped_rgb_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB)
    cropped_image_output = Image.from_ndarray(cropped_rgb_image)
   
    return Outputs(cropped_image=cropped_image_output)


