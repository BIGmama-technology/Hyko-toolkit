from pydantic import Field

from hyko_sdk.definitions import ToolkitModel
from hyko_sdk.metadata import CoreModel

func = ToolkitModel(
    name="fill_mask",
    task="natural_language_processing",
    description="Hugging Face fill mask task",
)


@func.set_startup_params
class StartupParams(CoreModel):
    hugging_face_model: str = Field(..., description="Model")
    device_map: str = Field(..., description="Device map (Auto, CPU or GPU)")


@func.set_input
class Inputs(CoreModel):
    masked_text: str = Field(..., description="Input text with <mask> to fill")


@func.set_param
class Params(CoreModel):
    top_k: int = Field(
        default=5, description="Number of top predictions to return (default: 5)."
    )


@func.set_output
class Outputs(CoreModel):
    sequence: list[str] = Field(..., description="Filled output text")
    score: list[float] = Field(..., description="Score of the filled sequence")
