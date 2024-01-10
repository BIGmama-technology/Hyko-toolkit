from pydantic import Field

from hyko_sdk.function import SDKFunction
from hyko_sdk.io import Image
from hyko_sdk.metadata import CoreModel

func = SDKFunction(
    description="OpenAI Dalle 2 image generation model (API)",
)


@func.set_input
class Inputs(CoreModel):
    prompt: str = Field(..., description="User text prompt")


@func.set_param
class Params(CoreModel):
    api_key: str = Field(..., description="OpenAI API KEY")


@func.set_output
class Outputs(CoreModel):
    generated_image: Image = Field(
        ..., description="AI Generated image from user text prompt"
    )
