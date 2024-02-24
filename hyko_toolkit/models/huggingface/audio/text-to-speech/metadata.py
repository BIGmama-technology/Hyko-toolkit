from pydantic import Field

from hyko_sdk.function import SDKFunction
from hyko_sdk.io import Audio
from hyko_sdk.metadata import CoreModel

func = SDKFunction(
    description="HuggingFace text to speech, run on cude may cause issues on cpu",
)


@func.set_startup_params
class StartupParams(CoreModel):
    hugging_face_model: str = Field(..., description="Model")
    device_map: str = Field(..., description="Device map (Auto, CPU or GPU)")


@func.set_input
class Inputs(CoreModel):
    text: str = Field(..., description="Input text")


@func.set_param
class Params(CoreModel):
    top_k: int = Field(
        default=1, description="Keep best k options (exploration vs. fluency)"
    )
    temperature: float = Field(
        default=0.5, description="Randomness (fluency vs. creativity)"
    )
    top_p: float = Field(
        default=0.5, description="Focus high-probability words (diversity control)"
    )


@func.set_output
class Outputs(CoreModel):
    speech: Audio = Field(..., description="Synthesized speech")
