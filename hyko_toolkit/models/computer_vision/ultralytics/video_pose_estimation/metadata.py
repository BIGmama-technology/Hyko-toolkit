from enum import Enum

from hyko_sdk.components.components import Slider
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.io import Video
from hyko_sdk.models import Category, CoreModel
from hyko_sdk.utils import field

func = ToolkitNode(
    name="Ultralytics video pose estimation",
    task="Computer vision",
    cost=0,
    description="UltraLytics Video Pose Estimation Using YOLO V8.",
    category=Category.MODEL,
)


class SupportedModels(str, Enum):
    yolov8n = "yolov8 Nano"
    yolov8s = "yolov8 Small"
    yolov8m = "yolov8 Medium"
    yolov8l = "yolov8 Large"
    yolov8x = "yolov8 XLarge"
    yolov8x_p6 = "yolov8 XP6"


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
        default=0.5,
        description="The probability necessary to make a prediction (default: 0.5).",
        component=Slider(leq=1, geq=0, step=0.01),
    )


@func.set_output
class Outputs(CoreModel):
    video: Video = field(description="Labeled Video.")
