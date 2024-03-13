from enum import Enum

from pydantic import Field

from hyko_sdk.definitions import ToolkitModel
from hyko_sdk.io import Video
from hyko_sdk.models import CoreModel

func = ToolkitModel(
    name="ultralytics_video_pose_estimation",
    task="computer_vision",
    description="UltraLytics Video Pose Estimation Using YOLO V8.",
)


class SupportedModels(str, Enum):
    yolov8n = "yolov8_Nano"
    yolov8s = "yolov8_Small"
    yolov8m = "yolov8_Medium"
    yolov8l = "yolov8_Large"
    yolov8x = "yolov8_XLarge"
    yolov8x_p6 = "yolov8_XP6"


@func.set_startup_params
class StartupParams(CoreModel):
    model: SupportedModels = Field(
        default="yolov8n-pose.pt", description="Yolo Models."
    )
    device_map: str = Field(default="cpu", description="Device map (Auto, CPU or GPU).")


@func.set_input
class Inputs(CoreModel):
    input_video: Video = Field(..., description="Input Video.")


@func.set_param
class Params(CoreModel):
    threshold: float = Field(
        default=0.5,
        description="The probability necessary to make a prediction (default: 0.5).",
    )


@func.set_output
class Outputs(CoreModel):
    video: Video = Field(..., description="Labeled Video.")
