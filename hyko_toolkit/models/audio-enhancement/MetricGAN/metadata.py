from pydantic import Field

from hyko_sdk.function import SDKFunction
from hyko_sdk.io import Audio
from hyko_sdk.metadata import CoreModel

func = SDKFunction(
    description="Enhance the quality of an audio recording. This model is designed to reduce noise and enhance the clarity of an audio file",
)


@func.set_startup_params
class StartupParams(CoreModel):
    device_map: str


@func.set_input
class Inputs(CoreModel):
    audio: Audio = Field(..., description="Audio input by the user for enhancement")


@func.set_param
class Params(CoreModel):
    pass


@func.set_output
class Outputs(CoreModel):
    enhanced: Audio = Field(..., description="Enhanced audio after processing")
