from hyko_sdk.components.components import Search, Slider
from hyko_sdk.io import Image
from hyko_sdk.models import Category, CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.callbacks_utils import huggingface_models_search
from hyko_toolkit.registry import ToolkitNode

func = ToolkitNode(
    name="Mask generation",
    task="Computer vision",
    cost=0,
    icon="hf",
    description="HuggingFace mask generation.",
    category=Category.MODEL,
)


@func.set_param
class Params(CoreModel):
    hugging_face_model: str = field(
        description="Model",
        component=Search(placeholder="Search mask generation model"),
    )
    device_map: str = field(default="cpu", description="Device map (Auto, CPU or GPU)")
    mask_threshold: float = field(
        default=0.0,
        description="Threshold to use when turning the predicted masks into binary values.",
        component=Slider(leq=1, geq=0, step=0.01),
    )
    points_per_batch: int = field(
        default=128,
        description="Sets the number of points run simultaneously by the model.",
        component=Slider(leq=128, geq=64, step=16),
    )
    pred_iou_thresh: float = field(
        default=0.95,
        description="A filtering threshold in [0,1] applied on the model's predicted mask quality.",
        component=Slider(leq=1, geq=0, step=0.01),
    )


@func.set_input
class Inputs(CoreModel):
    input_image: Image = field(description="Input image")


@func.set_output
class Outputs(CoreModel):
    bbox_img: Image = field(description="Boundig Boxes")
    mask_img: Image = field(description="Maskes")


func.callback(triggers=["hugging_face_model"], id="hugging_face_search")(
    huggingface_models_search
)
