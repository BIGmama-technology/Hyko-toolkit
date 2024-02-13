from io import BytesIO

from metadata import Inputs, Outputs, Params, func
from PyPDF2 import PdfReader


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    reader = PdfReader(BytesIO(inputs.pdf_file.get_data()))
    texts: list[str] = []

    for _, page in enumerate(reader.pages):
        texts.append(page.extract_text())

    text = "".join(texts)
    return Outputs(text=text)
