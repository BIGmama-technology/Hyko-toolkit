from pydantic import Field

from hyko_sdk.function import SDKFunction
from hyko_sdk.io import Audio
from hyko_sdk.metadata import CoreModel

func = SDKFunction(
    description="Generate audio from English text input",
)


@func.set_startup_params
class StartupParams(CoreModel):
    device_map: str = Field(default="auto", description="Device used")


@func.set_input
class Inputs(CoreModel):
    text: str = Field(
        ..., description="English text input provided by the user for speech generation"
    )


@func.set_param
class Params(CoreModel):
    pass


@func.set_output
class Outputs(CoreModel):
    audio: Audio = Field(
        ...,
        description="Generated audio containing the speech corresponding to the provided text",
    )
