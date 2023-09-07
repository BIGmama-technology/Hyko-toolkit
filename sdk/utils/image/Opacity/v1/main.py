from fastapi.exceptions import HTTPException
import numpy as np
from pydantic import Field
from hyko_sdk import CoreModel, SDKFunction, Image
import os
import cv2
from PIL import Image as PIL_Image


func = SDKFunction(
    description="Adjusts the opacity of an image",
    requires_gpu=False,
)

def convert_to_BGRA(image: np.ndarray, num_channels: int) -> np.ndarray:
    if num_channels == 3:
        return cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
    elif num_channels == 4:
        return image
    else:
        raise HTTPException(
            status_code=500,
            detail="Invalid number of input channels. Only 3 or 4 channels are supported."
        )


def opacity(img: np.ndarray, opacity: float) -> np.ndarray:
    h, w, c = img.shape
    if opacity == 100 and c == 4:
        return img
    imgout = convert_to_BGRA(img, c)
    opacity /= 100

    imgout[:, :, 3] *= opacity

    return imgout


class Inputs(CoreModel):
    image: Image = Field(..., description="Input image to adjust opacity")
   


class Params(CoreModel):
     opacity: float = Field(..., description="Opacity value (0-100)")


class Outputs(CoreModel):
    adjusted_image: Image = Field(..., description="Image with adjusted opacity")


@func.on_execute
async def main(inputs: Inputs , params: Params)-> Outputs:
   
    file, ext = os.path.splitext(inputs.image.get_name()) # type: ignore
    with open(f"./image{ext}", "wb") as f:
        f.write(inputs.image.get_data()) # type: ignore
    
    img_np = np.array(PIL_Image.open(f"./image{ext}"))

    opacity = params.opacity
    if not (0 <= opacity <= 100):
        raise HTTPException(status_code=500, detail="Opacity must be a percentage between 0 and 100.")
    

    h, w, c = img_np.shape
    if opacity == 100 and c == 4:
        adjusted_img_np = img_np
    else:
        imgout = convert_to_BGRA(img_np, c)
        opacity /= 100
        imgout[:, :, 3] = (imgout[:, :, 3] * opacity).astype(np.uint8)
        adjusted_img_np = imgout

  
    adjusted_image = Image.from_ndarray(adjusted_img_np)
   
    return Outputs(adjusted_image=adjusted_image)  
  