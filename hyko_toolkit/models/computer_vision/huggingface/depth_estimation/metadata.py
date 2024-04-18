from hyko_sdk.io import Image
from hyko_sdk.models import CoreModel
from pydantic import Field

from hyko_toolkit.registry import ToolkitModel

func = ToolkitModel(name='depth_estimation', task='computer_vision', description='HuggingFace depth estimation', absolute_dockerfile_path='./toolkit/hyko_toolkit/models/computer_vision/huggingface/Dockerfile', docker_context='./toolkit/hyko_toolkit/models/computer_vision/huggingface/depth_estimation')

@func.set_startup_params
class StartupParams(CoreModel):
    hugging_face_model: str = Field(..., description='Model')
    device_map: str = Field(..., description='Device map (Auto, CPU or GPU)')

@func.set_input
class Inputs(CoreModel):
    input_image: Image = Field(..., description='Input image')

@func.set_output
class Outputs(CoreModel):
    depth_map: Image = Field(..., description='Output depth map')
