from hyko_sdk.components.components import Slider
from hyko_sdk.io import Image
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.registry import ToolkitModel

func = ToolkitModel(
    name="image_segmentation",
    task="computer_vision",
    cost=0,
    description="HuggingFace image segmentation",
)


@func.set_input
class Inputs(CoreModel):
    input_image: Image = field(description="Input image")


@func.set_param
class Params(CoreModel):
    hugging_face_model: str = field(description="Model")
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


@func.set_output
class Outputs(CoreModel):
    mask: Image = field(description="Segmented image")
