import io

from hyko_sdk.models import CoreModel
from metadata import Inputs, Outputs, Params, func
from PIL import Image
from surya.model.detection.segformer import load_model as load_det_model
from surya.model.detection.segformer import load_processor as load_det_processor
from surya.model.recognition.model import load_model as load_rec_model
from surya.model.recognition.processor import load_processor as load_rec_processor
from surya.ocr import run_ocr


@func.on_startup
async def load(startup_params: CoreModel):
    global det_processor, det_model, rec_model, rec_processor

    det_processor, det_model = load_det_processor(), load_det_model()
    rec_model, rec_processor = load_rec_model(), load_rec_processor()


def ocr_surya(image_bytes: bytes, language: str):
    """
    Extracts text from an image using Surya-OCR.

    Args:
        image_bytes bytes: The image data in bytes.
        language (str, optional): The language code (e.g., 'en' for English, 'fr' for French).

    Returns:
        str: Extracted text from the image.
    """
    image = Image.open(io.BytesIO(image_bytes))

    predictions = run_ocr(
        [image], [[language]], det_model, det_processor, rec_model, rec_processor
    )
    mapped_texts = [
        text_line.text for item in predictions for text_line in item.text_lines
    ]
    return " ".join(mapped_texts)


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    generated_text = ocr_surya(
        await inputs.image.get_data(),
        language=params.language.value,
    )
    return Outputs(generated_text=generated_text)
