import io

import pytesseract
from PIL import Image

from .metadata import Inputs, Outputs, Params, node


def extract_text_from_image_bytes_tesseract(image_bytes: bytes, language: str):
    """
    Extracts text from an image using Tesseract OCR.

    Args:
        image_bytes bytes: The image data in bytes.
        language (str, optional): The language code (e.g., 'eng' for English, 'fra' for French).

    Returns:
        str: Extracted text from the image.
    """
    image = Image.open(io.BytesIO(image_bytes))

    extracted_text = pytesseract.image_to_string(image, lang=language)
    return extracted_text.strip()


@node.on_call
async def main(inputs: Inputs, params: Params) -> Outputs:
    generated_text = extract_text_from_image_bytes_tesseract(
        image_bytes=await inputs.image.get_data(),
        language=params.language.value,
    )
    return Outputs(generated_text=generated_text)
