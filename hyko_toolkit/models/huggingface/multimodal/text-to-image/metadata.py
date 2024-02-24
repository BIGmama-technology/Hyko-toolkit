from pydantic import Field

from hyko_sdk.function import SDKFunction
from hyko_sdk.io import Image
from hyko_sdk.metadata import CoreModel

func = SDKFunction(
    description="Hugging Face Text to Image Task",
)


@func.set_startup_params
class StartupParams(CoreModel):
    hugging_face_model: str = Field(..., description="Model")
    device_map: str = Field(..., description="Device map (Auto, CPU or GPU)")


@func.set_input
class Inputs(CoreModel):
    prompt: str = Field(..., description="Input text")
    image: Image = Field(..., description="Input Image")
    negative_prompt: str = Field(..., description="Input text")


@func.set_param
class Params(CoreModel):
    num_inference_steps: int = Field(
        default=15, description="The number of denoising steps."
    )
    strength: float = Field(
        default=0.8,
        description="Indicates extent to transform the reference image (between 0 and 1).",
    )
    guidance_scale: float = Field(
        default=7.5, description="Guidance scale influences image-text coherence.(> 1)"
    )


@func.set_output
class Outputs(CoreModel):
    generated_image: Image = Field(..., description="Generated image")
