from pydantic import Field

from hyko_sdk.function import SDKFunction
from hyko_sdk.metadata import CoreModel

func = SDKFunction(
    description="Hugging Face summarization",
)


@func.set_startup_params
class StartupParams(CoreModel):
    hugging_face_model: str = Field(..., description="Model")
    device_map: str = Field(..., description="Device map (Auto, CPU or GPU)")


@func.set_input
class Inputs(CoreModel):
    input_text: str = Field(..., description="text to summarize")


@func.set_param
class Params(CoreModel):
    max_length: int = Field(default=130, description="Maximum output length")


@func.set_output
class Outputs(CoreModel):
    summary_text: str = Field(..., description="Summary output")
