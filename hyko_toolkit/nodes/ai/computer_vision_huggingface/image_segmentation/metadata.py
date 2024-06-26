from hyko_sdk.components.components import Search, Slider
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.io import Image
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.callbacks_utils.huggingface_utils import huggingface_models_search

node = ToolkitNode(
    name="Image segmentation",
    cost=0,
    icon="hf",
    description="HuggingFace image segmentation",
    require_worker=True,
)


@node.set_param
class Params(CoreModel):
    hugging_face_model: str = field(
        description="Model",
        component=Search(placeholder="Search image segmentation model"),
    )
    device_map: str = field(description="Device map (Auto, CPU or GPU)")
    threshold: float = field(
        default=0.9,
        description="Probability threshold to filter out predicted masks.",
        component=Slider(leq=1, geq=0, step=0.01),
    )
    mask_threshold: float = field(
        default=0.5,
        description="Threshold to use when turning the predicted masks into binary values.",
        component=Slider(leq=1, geq=0, step=0.01),
    )
    overlap_mask_area_threshold: float = field(
        default=0.5,
        description="Mask overlap threshold to eliminate small, disconnected segments.",
        component=Slider(leq=1, geq=0, step=0.01),
    )


@node.set_input
class Inputs(CoreModel):
    input_image: Image = field(description="Input image")


@node.set_output
class Outputs(CoreModel):
    mask: Image = field(description="Segmented image")


node.callback(trigger="hugging_face_model", id="hugging_face_search")(
    huggingface_models_search
)
