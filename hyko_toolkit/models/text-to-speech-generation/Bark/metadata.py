from pydantic import Field

from hyko_sdk.function import SDKFunction
from hyko_sdk.io import Audio
from hyko_sdk.metadata import CoreModel

func = SDKFunction(
    description="Generate audio from a given prompt",
)


@func.set_startup_params
class StartupParams(CoreModel):
    pass


@func.set_input
class Inputs(CoreModel):
    text: str = Field(..., description="Prompt for audio generation")


@func.set_param
class Params(CoreModel):
    history: str = Field(
        default=None, description="History prompts for audio generation"
    )
    text_tempreture: float = Field(
        default=0.5,
        description="Generation temperature (1.0 more diverse, 0.0 more conservative)",
    )
    waveform_temp: float = Field(
        default=0.5,
        description="generation temperature (1.0 more diverse, 0.0 more conservative",
    )


@func.set_output
class Outputs(CoreModel):
    audio: Audio = Field(..., description="Generated audio")
