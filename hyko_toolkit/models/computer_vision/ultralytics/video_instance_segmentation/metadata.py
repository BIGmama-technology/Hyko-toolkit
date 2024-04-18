from enum import Enum

from hyko_sdk.io import Video
from hyko_sdk.models import CoreModel
from pydantic import Field

from hyko_toolkit.registry import ToolkitModel

func = ToolkitModel(name='ultralytics_video_instance_segmentation', task='computer_vision', description='UltraLytics Video instance segmentation Using YOLO segmentation V8.', absolute_dockerfile_path='./toolkit/hyko_toolkit/models/computer_vision/ultralytics/Dockerfile', docker_context='./toolkit/hyko_toolkit/models/computer_vision/ultralytics/video_instance_segmentation')

class SupportedModels(str, Enum):
    yolov8n = 'yolov8 Nano'
    yolov8s = 'yolov8 Small'
    yolov8m = 'yolov8 Medium'
    yolov8l = 'yolov8 Large'
    yolov8x = 'yolov8 XLarge'

@func.set_startup_params
class StartupParams(CoreModel):
    model: SupportedModels = Field(default=SupportedModels.yolov8n, description='Yolo Models.')
    device_map: str = Field(default='cpu', description='Device map (Auto, CPU or GPU).')

@func.set_input
class Inputs(CoreModel):
    input_video: Video = Field(..., description='Input Video.')

@func.set_param
class Params(CoreModel):
    threshold: float = Field(default=0.3, description='The probability necessary to make a prediction (default: 0.3).')

@func.set_output
class Outputs(CoreModel):
    video: Video = Field(..., description='Labeled Video.')
