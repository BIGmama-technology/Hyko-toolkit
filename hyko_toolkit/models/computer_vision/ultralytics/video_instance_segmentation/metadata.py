from enum import Enum

from hyko_sdk.definitions import ToolkitModel
from hyko_sdk.io import Video
from hyko_sdk.models import CoreModel
from pydantic import Field

func = ToolkitModel(
    name="ultralytics_video_instance_segmentation",
    task="computer_vision",
    description="UltraLytics Video instance segmentation Using YOLO segmentation V8.",
)


class SupportedModels(str, Enum):
    yolov8n = "yolov8_Nano"
    yolov8s = "yolov8_Small"
    yolov8m = "yolov8_Medium"
    yolov8l = "yolov8_Large"
    yolov8x = "yolov8_XLarge"


@func.set_startup_params
class StartupParams(CoreModel):
    model: SupportedModels = Field(
        default=SupportedModels.yolov8n, description="Yolo Models."
    )
    device_map: str = Field(default="cpu", description="Device map (Auto, CPU or GPU).")


@func.set_input
class Inputs(CoreModel):
    input_video: Video = Field(..., description="Input Video.")


@func.set_param
class Params(CoreModel):
    threshold: float = Field(
        default=0.3,
        description="The probability necessary to make a prediction (default: 0.3).",
    )


@func.set_output
class Outputs(CoreModel):
    video: Video = Field(..., description="Labeled Video.")