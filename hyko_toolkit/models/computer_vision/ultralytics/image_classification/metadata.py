from enum import Enum

from pydantic import Field

from hyko_sdk.definitions import ToolkitModel
from hyko_sdk.io import Image
from hyko_sdk.models import CoreModel

func = ToolkitModel(
    name="ultralytics_image_classification",
    task="computer_vision",
    description="UltraLytics Image Classification Using YOLOv8 Classifier.",
)


class SupportedModels(str, Enum):
    yolov8n = "yolov8_Nano"
    yolov8s = "yolov8_Small"
    yolov8m = "yolov8_Medium"
    yolov8l = "yolov8_Large"
    yolov8x = "yolov8_XLarge"


@func.set_startup_params
class StartupParams(CoreModel):
    model: SupportedModels = Field(default="yolov8n", description="Yolo Models.")
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
