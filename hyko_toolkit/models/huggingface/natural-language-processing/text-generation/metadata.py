from pydantic import Field

from hyko_sdk.function import SDKFunction
from hyko_sdk.metadata import CoreModel

func = SDKFunction(
    description="Hugging Face text generation",
)


@func.set_input
class Inputs(CoreModel):
    input_text: str = Field(..., description="input text")


@func.set_param
class Params(CoreModel):
    hugging_face_model: str = Field(..., description="Model")
    device_map: str = Field(..., description="Device map (Auto, CPU or GPU)")
    max_length: int = Field(
        default=30, description="maximum number of tokens to generate"
    )


@func.set_output
class Outputs(CoreModel):
    generated_text: str = Field(..., description="Completion text")
