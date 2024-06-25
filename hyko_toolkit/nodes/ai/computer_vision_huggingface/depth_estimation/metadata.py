from typing import Any

from hyko_sdk.components.components import Search
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.io import Image
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field
from pydantic import TypeAdapter

from hyko_toolkit.callbacks_utils.huggingface_utils import huggingface_models_search

ModelsAdapter = TypeAdapter(list[dict[str, Any]])

node = ToolkitNode(
    name="Depth estimation",
    cost=0,
    description="HuggingFace depth estimation",
    icon="hf",
    require_worker=True,
)


@node.set_param
class Params(CoreModel):
    hugging_face_model: str = field(
        description="Model",
        component=Search(placeholder="Search depth estimation model"),
    )
    device_map: str = field(description="Device map (Auto, CPU or GPU)")


@node.set_input
class Inputs(CoreModel):
    input_image: Image = field(description="Input image")


@node.set_output
class Outputs(CoreModel):
    depth_map: Image = field(description="Output depth map")


node.callback(trigger="hugging_face_model", id="hugging_face_search")(
    huggingface_models_search
)
