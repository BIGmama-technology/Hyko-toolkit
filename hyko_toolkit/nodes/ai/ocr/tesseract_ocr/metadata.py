from enum import Enum

from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.io import Image
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field


class SupportedLanguages(str, Enum):
    arabic = "ara"
    english = "eng"
    french = "fra"
    spanish = "spa"


func = ToolkitNode(
    name="Tesseract ocr",
    cost=0,
    description="Extracts text from an image using Tesseract OCR.",
)


@func.set_input
class Inputs(CoreModel):
    image: Image = field(description="The image you want to extract text from.")


@func.set_param
class Params(CoreModel):
    language: SupportedLanguages = field(
        default=SupportedLanguages.english.value,
        description="The language of the input image (default: en).",
    )


@func.set_output
class Outputs(CoreModel):
    generated_text: str = field(description="The Extracted text.")
