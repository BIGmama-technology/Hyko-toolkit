from enum import Enum

from hyko_sdk.io import Image
from hyko_sdk.models import Category, CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.registry import ToolkitNode


class SupportedLanguages(str, Enum):
    arabic = "ar"
    english = "en"
    french = "fr"
    spanish = "es"


func = ToolkitNode(
    name="Surya ocr",
    task="Optical character recognition",
    cost=0,
    description="Extracts text from an image using Surya-OCR.",
    category=Category.MODEL,
)


@func.set_input
class Inputs(CoreModel):
    image: Image = field(description="Your input image.")


@func.set_param
class Params(CoreModel):
    language: SupportedLanguages = field(
        default=SupportedLanguages.english.value,
        description="The language of the input image (default: en).",
    )


@func.set_output
class Outputs(CoreModel):
    generated_text: str = field(description="The Extracted text.")
