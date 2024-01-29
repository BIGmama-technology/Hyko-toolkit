import torch
from fastapi import HTTPException
from metadata import Inputs, Outputs, Params, func
from transformers import TrOCRProcessor, VisionEncoderDecoderModel

model = None
processor = None

device = torch.device("cuda:0") if torch.cuda.is_available() else torch.device("cpu")


@func.on_startup
async def load():
    global model
    global processor

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
