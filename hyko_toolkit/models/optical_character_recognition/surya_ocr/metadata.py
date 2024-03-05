from enum import Enum

from pydantic import Field

from hyko_sdk.function import SDKFunction
from hyko_sdk.io import Image
from hyko_sdk.metadata import CoreModel


class SupportedLanguages(str, Enum):
    arabic = "ar"
    english = "en"
    french = "fr"
    spanish = "es"


func = SDKFunction(
    description="Extracts text from an image using Surya-OCR.",
)


@func.set_startup_params
class StartupParams(CoreModel):
    pass


@func.set_input
class Inputs(CoreModel):
    image: Image = Field(..., description="Input image.")


@func.set_param
class Params(CoreModel):
    language: SupportedLanguages = Field(..., description="Select your language.")


@func.set_output
class Outputs(CoreModel):
    generated_text: str = Field(..., description="Extracted text.")
