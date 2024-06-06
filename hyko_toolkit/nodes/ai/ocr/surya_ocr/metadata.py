from enum import Enum

from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.io import Image
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field


class SupportedLanguages(str, Enum):
    arabic = "ar"
    english = "en"
    french = "fr"
    spanish = "es"


node = ToolkitNode(
    name="Surya ocr",
    description="Extracts text from an image using Surya-OCR.",
    icon="pdf",
    require_worker=True,
)


@node.set_input
class Inputs(CoreModel):
    image: Image = field(description="Your input image.")


@node.set_param
class Params(CoreModel):
    language: SupportedLanguages = field(
        default=SupportedLanguages.english.value,
        description="The language of the input image (default: en).",
    )


@node.set_output
class Outputs(CoreModel):
    generated_text: str = field(description="The Extracted text.")
