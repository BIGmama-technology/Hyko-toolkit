from enum import Enum

from hyko_sdk.components.components import Slider
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.io import Video
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

func = ToolkitNode(
    name="Ultralytics video object detection",
    cost=0,
    description="UltraLytics Video Object Detection Using YOLO V8 and V9.",
)


class SupportedModels(str, Enum):
    yolov8n = "yolov8 Nano"
    yolov8s = "yolov8 Small"
    yolov8m = "yolov8 Medium"
    yolov8l = "yolov8 Large"
    yolov8x = "yolov8 XLarge"
    yolov9c = "yolov9 compact"
    yolov9e = "yolov9 largest"


@func.set_input
class Inputs(CoreModel):
    input_video: Video = field(description="Input Video.")


@func.set_param
class Params(CoreModel):
    model: SupportedModels = field(
        default=SupportedModels.yolov8n, description="Yolo Models."
    )
    device_map: str = field(default="cpu", description="Device map (Auto, CPU or GPU).")
    threshold: float = field(
        default=0.3,
        description="The probability necessary to make a prediction (default: 0.3).",
        component=Slider(leq=1, geq=0, step=0.01),
    )
    iou_threshold: float = field(
        default=0.5,
        description="Intersection over union Threshold (IOU) (default: 0.5).",
        component=Slider(leq=1, geq=0, step=0.01),
    )


@func.set_output
class Outputs(CoreModel):
    video: Video = field(description="Labeled Video.")