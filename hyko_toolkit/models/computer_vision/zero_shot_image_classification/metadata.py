from hyko_sdk.definitions import ToolkitModel
from hyko_sdk.io import Image
from hyko_sdk.models import CoreModel
from pydantic import Field

func = ToolkitModel(
    name="zero_shot_image_classification",
    task="computer_vision",
    description="Hugging Face image classification",
)


@func.set_startup_params
class StartupParams(CoreModel):
    hugging_face_model: str = Field(..., description="Model")
    device_map: str = Field(..., description="Device map (Auto, CPU or GPU)")


@func.set_input
class Inputs(CoreModel):
    input_image: Image = Field(..., description="Input image")
    labels: list[str] = Field(..., description="Labels for classification")


@func.set_param
class Params(CoreModel):
    hypothesis_template: str = Field(
        default="This is a photo of {}",
        description="Template for image classification hypothesis.",
    )


@func.set_output
class Outputs(CoreModel):
    labels: list[str] = Field(..., description="Class of the image.")
    scores: list[float] = Field(..., description="Scores for each class.")
