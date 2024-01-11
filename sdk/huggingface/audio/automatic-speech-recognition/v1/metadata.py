from pydantic import Field

from hyko_sdk.function import SDKFunction
from hyko_sdk.io import Audio
from hyko_sdk.metadata import CoreModel

func = SDKFunction(
    description="HuggingFace automatic speech recognition",
)


@func.set_input
class Inputs(CoreModel):
    speech: Audio = Field(..., description="Input speech")


@func.set_param
class Params(CoreModel):
    hugging_face_model: str = Field(..., description="Model")
    device_map: str = Field(..., description="Device map (Auto, CPU or GPU)")


@func.set_output
class Outputs(CoreModel):
    text: str = Field(..., description="Recognized speech text")
