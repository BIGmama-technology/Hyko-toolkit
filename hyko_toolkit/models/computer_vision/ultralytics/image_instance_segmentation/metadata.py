from enum import Enum

from hyko_sdk.components.components import Slider
from hyko_sdk.io import Image
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.registry import ToolkitModel

func = ToolkitModel(
    name="ultralytics_image_instance_segmentation",
    task="computer_vision",
    description="UltraLytics Instance Segmentation Using YOLO segmentation V8.",
    absolute_dockerfile_path="./toolkit/hyko_toolkit/models/computer_vision/ultralytics/Dockerfile",
    docker_context="./toolkit/hyko_toolkit/models/computer_vision/ultralytics/image_instance_segmentation",
)


class SupportedModels(str, Enum):
    yolov8n = "yolov8 Nano"
    yolov8s = "yolov8 Small"
    yolov8m = "yolov8 Medium"
    yolov8l = "yolov8 Large"
    yolov8x = "yolov8 XLarge"


@func.set_startup_params
class StartupParams(CoreModel):
    model: SupportedModels = field(
        default=SupportedModels.yolov8n, description="Yolo Models."
    )
    device_map: str = field(default="cpu", description="Device map (Auto, CPU or GPU).")


@func.set_input
class Inputs(CoreModel):
    input_image: Image = field(description="Input image.")


@func.set_param
class Params(CoreModel):
    threshold: float = field(
        default=0.5,
        description="The probability necessary to make a prediction (default: 0.5).",
        component=Slider(leq=0, geq=1, step=0.01),
    )


@func.set_output
class Outputs(CoreModel):
    image: Image = field(description="Labeled image.")
