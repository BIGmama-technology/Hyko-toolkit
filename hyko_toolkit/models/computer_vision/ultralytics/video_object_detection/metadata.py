from enum import Enum

from pydantic import Field

from hyko_sdk.definitions import ToolkitModel
from hyko_sdk.io import Video
from hyko_sdk.models import CoreModel

func = ToolkitModel(
    name="ultralytics_video_object_detection",
    task="computer_vision",
    description="UltraLytics Video Object Detection Using YOLO V8.",
)


class SupportedModels(str, Enum):
    yolov8n = "yolov8_Nano"
    yolov8m = "yolov8_Medium"
    yolov8l = "yolov8_Large"


@func.set_startup_params
class StartupParams(CoreModel):
    model: SupportedModels = Field(..., description="Yolo Models.")


@func.set_input
class Inputs(CoreModel):
    input_video: Video = Field(..., description="Input Video.")


@func.set_param
class Params(CoreModel):
    threshold: float = Field(
        default=0.5,
        description="The probability necessary to make a prediction (default: 0.5).",
    )
    iou_threshold: float = Field(
        default=0.5,
        description="Intersection over union Threshold (IOU) (default: 0.5).",
    )


@func.set_output
class Outputs(CoreModel):
    video: Video = Field(..., description="Labeled Video.")
