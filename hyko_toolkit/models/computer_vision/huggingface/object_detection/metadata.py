from hyko_sdk.components.components import Search, Slider
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.io import Image
from hyko_sdk.models import Category, CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.callbacks_utils.huggingface_utils import huggingface_models_search

func = ToolkitNode(
    name="Object detection",
    task="Computer vision",
    cost=0,
    icon="hf",
    description="Hugging face object detection",
    category=Category.MODEL,
)


@func.set_input
class Inputs(CoreModel):
    input_image: Image = field(description="Input image.")


@func.set_param
class Params(CoreModel):
    hugging_face_model: str = field(
        description="Model",
        component=Search(placeholder="Search object detection model"),
    )
    device_map: str = field(description="Device map (Auto, CPU or GPU).")
    threshold: float = field(
        default=0.7,
        description="The probability necessary to make a prediction.",
        component=Slider(leq=1, geq=0, step=0.01),
    )


@func.set_output
class Outputs(CoreModel):
    final: Image = field(description="Labeled image.")


func.callback(trigger="hugging_face_model", id="hugging_face_search")(
    huggingface_models_search
)
