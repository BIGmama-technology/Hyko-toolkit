import os
from io import BytesIO

import fitz  # PyMuPDF
import pytesseract
from PIL import Image

from .metadata import Inputs, Outputs, Params, func


@func.on_call
async def main(inputs: Inputs, params: Params) -> Outputs:
    """
    Perform OCR (Optical Character Recognition) on a PDF document.

    Args:
        pdf_path (str): The path to the PDF file.
        language (str): The language code for OCR (e.g., 'eng' for English, 'fra' for French, 'ara' for Arabic).

    Returns:
        str: The extracted text from the PDF document.
    """
    pdf_bytes_io = BytesIO(await inputs.pdf_file.get_data())
    with open("file.pdf", "wb") as file:
        file.write(pdf_bytes_io.getbuffer())
    text_list = []
    # Open the PDF file
    doc = fitz.open("file.pdf")
    # Convert each page to an image and perform OCR
    for page_num in range(doc.page_count):  # doc.page_count
        # Convert the current page to an image
        page = doc.load_page(page_num)
        pix = page.get_pixmap(matrix=fitz.Matrix(300 / 72, 300 / 72))
        temp_image_path = f"page_{page_num}.png"
        image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        image.save(temp_image_path)
        text = (
            pytesseract.image_to_string(
                Image.open(temp_image_path), lang=params.language
            )
            + " "
        )
        text_list.append(text)
        # Remove the temporary image file
        os.remove(temp_image_path)
    doc.close()
    text_list_str = " ".join(text_list)
    return Outputs(text=text_list_str)
