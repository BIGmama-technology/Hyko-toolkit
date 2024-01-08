import torch
from fastapi import HTTPException
from pydantic import Field
from transformers import TrOCRProcessor, VisionEncoderDecoderModel

from hyko_sdk.function import SDKFunction
from hyko_sdk.io import Image
from hyko_sdk.metadata import CoreModel

func = SDKFunction(
    description="Perform Handwritten Text Recognition on an input image",
    requires_gpu=False,
)


class Inputs(CoreModel):
    image: Image = Field(..., description="Input image containing handwritten text")


class Params(CoreModel):
    pass


class Outputs(CoreModel):
    generated_text: str = Field(..., description="Recognized text from the input image")


model = None
processor = None

device = torch.device("cuda:0") if torch.cuda.is_available() else torch.device("cpu")


@func.on_startup
async def load():
    global model
    global processor
    if model is not None and processor is not None:
        print("Model loaded already")
        return

    processor = TrOCRProcessor.from_pretrained("microsoft/trocr-large-handwritten")
    model = VisionEncoderDecoderModel.from_pretrained(
        "microsoft/trocr-large-handwritten"
    )


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    if model is None or processor is None:
        raise HTTPException(status_code=500, detail="Model is not loaded yet")

    img = inputs.image.to_ndarray()

    pixel_values = processor(images=img, return_tensors="pt").pixel_values

    with torch.no_grad():
        generated_ids = model.generate(pixel_values)

    generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

    return Outputs(generated_text=generated_text)
