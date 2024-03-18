from enum import Enum

from hyko_sdk.definitions import ToolkitModel
from hyko_sdk.io import Image
from hyko_sdk.models import CoreModel
from pydantic import Field

func = ToolkitModel(
    name="ultralytics_image_classification",
    task="computer_vision",
    description="UltraLytics Image Classification Using YOLOv8 Classifier.",
)


class SupportedModels(str, Enum):
    yolov8n = "yolov8 Nano"
    yolov8s = "yolov8 Small"
    yolov8m = "yolov8 Medium"
    yolov8l = "yolov8 Large"
    yolov8x = "yolov8 XLarge"


@func.set_startup_params
class StartupParams(CoreModel):
    model: SupportedModels = Field(
        default=SupportedModels.yolov8n, description="Yolo Models."
    )
    device_map: str = Field(default="cpu", description="Device map (Auto, CPU or GPU).")


@func.set_input
class Inputs(CoreModel):
    input_image: Image = Field(..., description="Input image.")


@func.set_param
class Params(CoreModel):
    threshold: float = Field(
        default=0.5,
        description="The probability necessary to make a prediction (default: 0.5).",
    )


@func.set_output
class Outputs(CoreModel):
    top5_class_names: list[str] = Field(..., description="Top 5 Class names.")
    top5_conf: list[float] = Field(..., description="Top 5 confidence values.")
