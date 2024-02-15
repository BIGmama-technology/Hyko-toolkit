from io import BytesIO

from langchain_community.document_loaders import PyPDFLoader
from metadata import Inputs, Outputs, Params, func


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    pdf_bytes_io = BytesIO(inputs.pdf_file.get_data())
    with open("file.pdf", "wb") as file:
        file.write(pdf_bytes_io.getbuffer())
    loader = PyPDFLoader("file.pdf", extract_images=False)  # type: ignore
    pages = loader.load()
    result = [i.page_content for i in pages]
    result_text = " ".join(result)
    return Outputs(text=result_text)
