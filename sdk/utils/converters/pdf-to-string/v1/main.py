from io import BytesIO
from pydantic import Field
from hyko_sdk import CoreModel, SDKFunction, PDF
from PyPDF2 import PdfReader

func = SDKFunction(
    description="Convert a PDF type to String type (extracts the text from the pdf)",
    requires_gpu=False,
)

class Inputs(CoreModel):
    pdf_file: PDF = Field(..., description="User input pdf to be converted to text")

class Params(CoreModel):
    pass

class Outputs(CoreModel):
    text: str = Field(..., description="Extracted text from pdf")


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    reader = PdfReader(BytesIO(inputs.pdf_file.get_data()))
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return Outputs(text=text)
