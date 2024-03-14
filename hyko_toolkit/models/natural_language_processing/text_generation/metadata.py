from hyko_sdk.definitions import ToolkitModel
from hyko_sdk.models import CoreModel
from pydantic import Field

func = ToolkitModel(
    name="text_generation",
    task="natural_language_processing",
    description="Hugging Face text generation",
)


@func.set_startup_params
class StartupParams(CoreModel):
    hugging_face_model: str = Field(..., description="Model")
    device_map: str = Field(..., description="Device map (Auto, CPU or GPU)")


@func.set_input
class Inputs(CoreModel):
    input_text: str = Field(..., description="input text")


@func.set_param
class Params(CoreModel):
    max_new_tokens: int = Field(
        default=30, description="Cap newly generated content length"
    )
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
    generated_text: str = Field(..., description="Completion text")
