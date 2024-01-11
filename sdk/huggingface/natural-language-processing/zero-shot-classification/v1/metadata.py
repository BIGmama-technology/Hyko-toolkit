from pydantic import Field

from hyko_sdk.function import SDKFunction
from hyko_sdk.metadata import CoreModel

func = SDKFunction(
    description="Hugging Face Zero Shot Classification Task",
)


@func.set_input
class Inputs(CoreModel):
    input_text: str = Field(..., description="Input text")
    candidate_labels: list[str] = Field(
        ..., description="Candidate labels to use for classification"
    )


@func.set_param
class Params(CoreModel):
    hugging_face_model: str = Field(..., description="Model")
    device_map: str = Field(..., description="Device map (Auto, CPU or GPU)")


@func.set_output
class Outputs(CoreModel):
    labels: list[str] = Field(..., description="Classified labels")
    scores: list[float] = Field(..., description="Respective classification scores")
