from pydantic import Field

from hyko_sdk.function import SDKFunction
from hyko_sdk.io import Image
from hyko_sdk.metadata import CoreModel

func = SDKFunction(
    description="Hugging Face image captioning",
)


@func.set_startup_params
class StartupParams(CoreModel):
    hugging_face_model: str = Field(..., description="Model")
    device_map: str = Field(..., description="Device map (Auto, CPU or GPU)")


@func.set_input
class Inputs(CoreModel):
    input_image: Image = Field(..., description="Input image")


@func.set_param
class Params(CoreModel):
    max_new_tokens: int = Field(
        default=20, description="Cap newly generated content length (default=20)."
    )
    temperature: float = Field(default=0.6, description="Randomness (default=0.8).")
    top_p: float = Field(
        default=0.7, description="Focus high-probability words (default=0.7)"
    )
    top_k: int = Field(default=1, description="Keep best k options (default=1).")


@func.set_output
class Outputs(CoreModel):
    caption: str = Field(..., description="Image caption")
