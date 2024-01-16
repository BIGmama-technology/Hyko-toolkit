from pydantic import Field

from hyko_sdk.function import SDKFunction
from hyko_sdk.io import Video
from hyko_sdk.metadata import CoreModel

func = SDKFunction(
    description="HuggingFace video classification",
)


@func.set_input
class Inputs(CoreModel):
    input_video: Video = Field(..., description="Input image")


@func.set_param
class Params(CoreModel):
    hugging_face_model: str = Field(..., description="Model")
    device_map: str = Field(..., description="Device map (Auto, CPU or GPU)")


@func.set_output
class Outputs(CoreModel):
    summary: str = Field(..., description="Summary of results")
