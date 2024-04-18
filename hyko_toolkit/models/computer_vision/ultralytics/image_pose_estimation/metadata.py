from enum import Enum

from hyko_sdk.io import Image
from hyko_sdk.models import CoreModel
from pydantic import Field

from hyko_toolkit.registry import ToolkitModel

func = ToolkitModel(name='ultralytics_image_pose_estimation', task='computer_vision', description='UltraLytics Image Pose Estimation Using YOLO V8.', absolute_dockerfile_path='./toolkit/hyko_toolkit/models/computer_vision/ultralytics/Dockerfile', docker_context='./toolkit/hyko_toolkit/models/computer_vision/ultralytics/image_pose_estimation')

class SupportedModels(str, Enum):
    yolov8n = 'yolov8 Nano'
    yolov8s = 'yolov8 Small'
    yolov8m = 'yolov8 Medium'
    yolov8l = 'yolov8 Large'
    yolov8x = 'yolov8 XLarge'
    yolov8x_p6 = 'yolov8 XP6'

@func.set_startup_params
class StartupParams(CoreModel):
    model: SupportedModels = Field(default=SupportedModels.yolov8n, description='Yolo Models.')
    device_map: str = Field(default='cpu', description='Device map (Auto, CPU or GPU).')

@func.set_input
class Inputs(CoreModel):
    input_image: Image = Field(..., description='Input image.')

@func.set_param
class Params(CoreModel):
    threshold: float = Field(default=0.5, description='The probability necessary to make a prediction (default: 0.5).')
    iou_threshold: float = Field(default=0.5, description='Intersection over union Threshold (IOU) (default: 0.5).')

@func.set_output
class Outputs(CoreModel):
    image: Image = Field(..., description='Labeled image.')
