from enum import Enum

from hyko_sdk.definitions import ToolkitModel
from hyko_sdk.io import Image
from hyko_sdk.models import CoreModel
from pydantic import Field


class SupportedLanguages(str, Enum):
    arabic = "ara"
    english = "eng"
    french = "fra"
    spanish = "spa"


func = ToolkitModel(
    name="tesseract_ocr",
    task="optical_character_recognition",
    description="Extracts text from an image using Tesseract OCR.",
)


@func.set_input
class Inputs(CoreModel):
    image: Image = Field(..., description="Input image.")


@func.set_param
class Params(CoreModel):
    language: SupportedLanguages = Field(
        default=SupportedLanguages.english.value, description="Select your language."
    )


@func.set_output
class Outputs(CoreModel):
    generated_text: str = Field(..., description="Extracted text.")
