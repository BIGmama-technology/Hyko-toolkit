from typing import Any

from hyko_sdk.components.components import Search
from hyko_sdk.io import Image
from hyko_sdk.models import CoreModel, ModelMetaData
from hyko_sdk.utils import field
from pydantic import TypeAdapter

from hyko_toolkit.callbacks_utils import huggingface_models_search
from hyko_toolkit.registry import ToolkitModel

ModelsAdapter = TypeAdapter(list[dict[str, Any]])

func = ToolkitModel(
    name="depth-estimation",
    task="computer_vision",
    cost=0,
    description="HuggingFace depth estimation",
    absolute_dockerfile_path="./toolkit/hyko_toolkit/models/computer_vision/huggingface/Dockerfile",
    docker_context="./toolkit/hyko_toolkit/models/computer_vision/huggingface/depth_estimation",
)


@func.set_startup_params
class StartupParams(CoreModel):
    hugging_face_model: str = field(
        description="Model",
        component=Search(placeholder="Search depth estimation model"),
    )
    device_map: str = field(description="Device map (Auto, CPU or GPU)")


@func.set_input
class Inputs(CoreModel):
    input_image: Image = field(description="Input image")


@func.set_output
class Outputs(CoreModel):
    depth_map: Image = field(description="Output depth map")


@func.callback(triggers=["hugging_face_model"], id="depth_estimation_search")
async def add_search_results(
    metadata: ModelMetaData, access_token: str, refresh_token: str
) -> ModelMetaData:
    return await huggingface_models_search(metadata)
