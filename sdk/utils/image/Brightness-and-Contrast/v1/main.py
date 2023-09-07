from pydantic import Field
from hyko_sdk import CoreModel, Image, SDKFunction
import numpy as np
import cv2


func = SDKFunction(
    description="Adjust brightness and contrast of an image",
    requires_gpu=False,
)

class Inputs(CoreModel):
    image: Image = Field(..., description="Input image to adjust brightness and contrast")

class Params(CoreModel):
    brightness: float = Field(..., description="Brightness adjustment factor (e.g., 1.0 for no change)")
    contrast: float = Field(..., description="Contrast adjustment factor (e.g., 1.0 for no change)")

class Outputs(CoreModel):
    adjusted_image: Image = Field(..., description="Image with adjusted brightness and contrast")

@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
   
    img_np = inputs.image.to_ndarray()
   
    image_cv2 = cv2.cvtColor(np.array(img_np), cv2.COLOR_RGB2BGR)
    
    adjusted_image = cv2.convertScaleAbs(image_cv2, alpha=params.contrast, beta=params.brightness)
    adjusted_rgb_image = cv2.cvtColor(adjusted_image, cv2.COLOR_BGR2RGB)

    image = Image.from_ndarray(adjusted_rgb_image)
   
    return Outputs(adjusted_image=image)
