import numpy as np
import RRDBNet_arch as arch
import torch
from fastapi import HTTPException
from pydantic import Field

from hyko_sdk.function import SDKFunction
from hyko_sdk.io import Image
from hyko_sdk.metadata import CoreModel

func = SDKFunction(
    description="Enhance the resolution of an image. This model improves the quality and sharpness of an image by increasing its resolution",
    requires_gpu=False,
)


class Inputs(CoreModel):
    image: Image = Field(..., description="Input image to be enhanced")


class Params(CoreModel):
    pass


class Outputs(CoreModel):
    enhanced_image: Image = Field(..., description="Enhanced resolution image")


model = None

device = torch.device("cuda:0") if torch.cuda.is_available() else torch.device("cpu")


@func.on_startup
async def load():
    global model

    if model is not None:
        print("Model loaded already")
        return

    model_path = "./RRDB_ESRGAN_x4.pth"

    model = arch.RRDBNet(3, 3, 64, 23, gc=32)
    model.load_state_dict(torch.load(model_path), strict=True)
    model.eval()
    model = model.to(device)


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    if model is None:
        raise HTTPException(status_code=500, detail="Model is not loaded yet")

    image = inputs.image.to_ndarray()

    img = np.array(image)

    img = img * 1.0 / 255  # type: ignore
    img = torch.from_numpy(np.transpose(img[:, :, [2, 1, 0]], (2, 0, 1))).float()
    img_LR = img.unsqueeze(0)
    img_LR = img_LR.to(device)

    with torch.no_grad():
        output = model(img_LR).data.squeeze().float().cpu().clamp_(0, 1).numpy()

    output = np.transpose(output[[2, 1, 0], :, :], (1, 2, 0))
    output = (output * 255.0).round().astype(np.uint8)

    img = Image.from_ndarray(output)

    return Outputs(enhanced_image=img)
