from hyko_sdk.components.components import Search
from hyko_sdk.io import Image
from hyko_sdk.models import CoreModel, ModelMetaData
from hyko_sdk.utils import field
from pydantic import Field

from hyko_toolkit.callbacks_utils import huggingface_models_search
from hyko_toolkit.registry import ToolkitModel

func = ToolkitModel(
    name="object_detection",
    task="computer_vision",
    description="Hugging face object detection",
    absolute_dockerfile_path="./toolkit/hyko_toolkit/models/computer_vision/huggingface/object_detection/Dockerfile",
    docker_context="./toolkit/hyko_toolkit/models/computer_vision/huggingface/object_detection",
)


@func.set_startup_params
class StartupParams(CoreModel):
    hugging_face_model: str = field(
        description="Model",
        component=Search(placeholder="Search object detection model"),
    )
    device_map: str = Field(..., description="Device map (Auto, CPU or GPU).")


@func.set_input
class Inputs(CoreModel):
    input_image: Image = Field(..., description="Input image.")


@func.set_param
class Params(CoreModel):
    threshold: float = Field(
        default=0.7, description="The probability necessary to make a prediction."
    )


@func.set_output
class Outputs(CoreModel):
    final: Image = Field(..., description="Labeled image.")


@func.callback(triggers=["hugging_face_model"], id="object_detection_search")
async def add_search_results(
    metadata: ModelMetaData, access_token: str, refresh_token: str
) -> ModelMetaData:
    return await huggingface_models_search(metadata)
