import easyocr
from metadata import Inputs, Outputs, Params, func


def extract_text_from_image_bytes(image_bytes: bytes, language: str):
    """
    Extracts text from an image using EasyOCR.

    Args:
        image_bytes (bytes): The image data in bytes.
        language (str): The language code (eg : 'en' for english,'fr' for french).

    Returns:
        str: Extracted text from the image.
    """
    reader = easyocr.Reader([language])
    result = reader.readtext(image_bytes)
    extracted_text = ""
    for detection in result:
        text = detection[1]
        extracted_text += text + " "

    return extracted_text.strip()


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    generated_text = extract_text_from_image_bytes(
        image_bytes=inputs.image.get_data(), language=params.language.value
    )
    return Outputs(generated_text=generated_text)
