from enum import Enum

from hyko_sdk.io import Image
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.registry import ToolkitModel


class SupportedLanguages(str, Enum):
    arabic = "ara"
    english = "eng"
    french = "fra"
    spanish = "spa"


func = ToolkitModel(
    name="Tesseract ocr",
    task="Optical character recognition",
    cost=0,
    description="Extracts text from an image using Tesseract OCR.",
    absolute_dockerfile_path="./toolkit/hyko_toolkit/models/optical_character_recognition/tesseract_ocr/Dockerfile",
    docker_context="./toolkit/hyko_toolkit/models/optical_character_recognition/tesseract_ocr",
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
