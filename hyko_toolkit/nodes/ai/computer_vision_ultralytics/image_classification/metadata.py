from enum import Enum

from hyko_sdk.components.components import Slider
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.io import Image
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

node = ToolkitNode(
    name="Ultralytics image classification",
    cost=0,
    description="UltraLytics Image Classification Using YOLOv8 Classifier.",
    require_worker=True,
)


class SupportedModels(str, Enum):
    yolov8n = "yolov8 Nano"
    yolov8s = "yolov8 Small"
    yolov8m = "yolov8 Medium"
    yolov8l = "yolov8 Large"
    yolov8x = "yolov8 XLarge"


@node.set_input
class Inputs(CoreModel):
    input_image: Image = field(description="Input image.")


@node.set_param
class Params(CoreModel):
    model: SupportedModels = field(
        default=SupportedModels.yolov8n, description="Yolo Models."
    )
    device_map: str = field(default="cpu", description="Device map (Auto, CPU or GPU).")
    threshold: float = field(
        default=0.5,
        description="The probability necessary to make a prediction (default: 0.5).",
        component=Slider(leq=1, geq=0, step=0.01),
    )


@node.set_output
class Outputs(CoreModel):
    top5_class_names: list[str] = field(description="Top 5 Class names.")
    top5_conf: list[float] = field(description="Top 5 confidence values.")
