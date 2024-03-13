from pydantic import Field

from hyko_sdk.definitions import ToolkitModel
from hyko_sdk.models import CoreModel

func = ToolkitModel(
    name="text_classification",
    task="natural_language_processing",
    description="Hugging Face text classification",
)


@func.set_startup_params
class StartupParams(CoreModel):
    hugging_face_model: str = Field(..., description="Model")
    device_map: str = Field(..., description="Device map (Auto, CPU or GPU)")


@func.set_input
class Inputs(CoreModel):
    input_text: list[str] = Field(..., description="Text to classify.")


@func.set_param
class Params(CoreModel):
    pass


@func.set_output
class Outputs(CoreModel):
    label: list[str] = Field(..., description="Class labels")
    score: list[float] = Field(..., description="Associated score to the class label")
