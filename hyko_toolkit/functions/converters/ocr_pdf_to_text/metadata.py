from enum import Enum

from hyko_sdk.io import PDF
from hyko_sdk.models import Category, CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.registry import ToolkitNode


class SupportedLanguages(str, Enum):
    english = "eng"
    arabic = "ara"
    french = "fra"


func = ToolkitNode(
    name="OCR pdf to text",
    task="Converters",
    category=Category.FUNCTION,
    cost=3,
    description="Perform OCR (Optical Character Recognition) on a PDF document",
    icon="pdf",
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
