from io import BytesIO

from hyko_sdk.models import CoreModel
from langchain_community.document_loaders import PyPDFLoader
from metadata import Inputs, Outputs, func


@func.on_execute
async def main(inputs: Inputs, params: CoreModel) -> Outputs:
    """
    Processes a PDF file provided in binary format, extracts text content from it,
    and returns the concatenated text as output.

    Args:
        inputs (Inputs): Input data containing the PDF file in binary format.
        params (Params): Parameters for the function (not used in this function).

    Returns:
        Outputs: Extracted text content from the PDF file.
    """
    pdf_bytes_io = BytesIO(await inputs.pdf_file.get_data())
    with open("file.pdf", "wb") as file:
        file.write(pdf_bytes_io.getbuffer())
    loader = PyPDFLoader("file.pdf", extract_images=False)  # type: ignore
    pages = loader.load()
    result = [i.page_content for i in pages]
    result_text = " ".join(result)
    return Outputs(text=result_text)
