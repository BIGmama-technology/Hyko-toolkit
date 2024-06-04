from typing import Any

from hyko_sdk.components.components import Search
from hyko_sdk.io import Image
from hyko_sdk.models import Category, CoreModel
from hyko_sdk.utils import field
from pydantic import TypeAdapter

from hyko_toolkit.callbacks_utils.huggingface_utils import huggingface_models_search
from hyko_toolkit.registry import ToolkitNode

ModelsAdapter = TypeAdapter(list[dict[str, Any]])

func = ToolkitNode(
    name="Depth estimation",
    task="Computer vision",
    cost=0,
    description="HuggingFace depth estimation",
    icon="hf",
    category=Category.MODEL,
)


@func.set_param
class Params(CoreModel):
    hugging_face_model: str = field(
        description="Model",
        component=Search(placeholder="Search depth estimation model"),
    )
    device_map: str = field(description="Device map (Auto, CPU or GPU)")
    test: bool = field(description="Test")


@func.set_input
class Inputs(CoreModel):
    input_image: Image = field(description="Input image")


@func.set_output
class Outputs(CoreModel):
    depth_map: Image = field(description="Output depth map")


func.callback(trigger="hugging_face_model", id="hugging_face_search")(
    huggingface_models_search
)
