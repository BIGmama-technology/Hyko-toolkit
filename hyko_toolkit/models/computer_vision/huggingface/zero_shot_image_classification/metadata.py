from hyko_sdk.components.components import Search
from hyko_sdk.io import Image
from hyko_sdk.models import CoreModel, ModelMetaData
from hyko_sdk.utils import field
from pydantic import Field

from hyko_toolkit.callbacks_utils import huggingface_models_search
from hyko_toolkit.registry import ToolkitModel

func = ToolkitModel(
    name="zero_shot_image_classification",
    task="computer_vision",
    description="Hugging Face image classification",
    absolute_dockerfile_path="./toolkit/hyko_toolkit/models/computer_vision/huggingface/Dockerfile",
    docker_context="./toolkit/hyko_toolkit/models/computer_vision/huggingface/zero_shot_image_classification",
)


@func.set_startup_params
class StartupParams(CoreModel):
    hugging_face_model: str = field(
        description="Model",
        component=Search(placeholder="Search zero shot image classification model"),
    )
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


@func.callback(
    triggers=["hugging_face_model"], id="zero_shot_image_classification_search"
)
async def add_search_results(
    metadata: ModelMetaData, access_token: str, refresh_token: str
) -> ModelMetaData:
    return await huggingface_models_search(metadata)
