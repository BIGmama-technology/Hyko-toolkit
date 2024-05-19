from enum import Enum

from hyko_sdk.io import PDF
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.registry import ToolkitFunction


class SupportedLanguages(str, Enum):
    english = "eng"
    arabic = "ara"
    french = "fra"


func = ToolkitFunction(
    name="ocr_pdf_to_text",
    task="converters",
    cost=3,
    description="Perform OCR (Optical Character Recognition) on a PDF document",
    absolute_dockerfile_path="./toolkit/hyko_toolkit/functions/converters/ocr_pdf_to_text/Dockerfile",
    docker_context="./toolkit/hyko_toolkit/functions/converters/ocr_pdf_to_text",
)


@func.set_input
class Inputs(CoreModel):
    pdf_file: PDF = field(description="User input pdf to be converted to text")


@func.set_param
class Params(CoreModel):
    language: SupportedLanguages = field(description="Select PDF language.")


@func.set_output
class Outputs(CoreModel):
    text: str = field(description="Extracted text from pdf .")
