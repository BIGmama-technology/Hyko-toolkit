from hyko_sdk.io import Image
from hyko_sdk.models import CoreModel
from pydantic import Field

from hyko_toolkit.registry import ToolkitModel

func = ToolkitModel(name='visual_question_answering', task='multimodal', description='Hugging Face Image-To-Text Task', absolute_dockerfile_path='./toolkit/hyko_toolkit/models/multimodal/Dockerfile', docker_context='./toolkit/hyko_toolkit/models/multimodal/visual_question_answering')

@func.set_startup_params
class StartupParams(CoreModel):
    hugging_face_model: str = Field(..., description='Model')
    device_map: str = Field(..., description='Device map (Auto, CPU or GPU)')

@func.set_input
class Inputs(CoreModel):
    image: Image = Field(..., description='Input image')
    question: str = Field(..., description='Input question')

@func.set_param
class Params(CoreModel):
    top_k: int = Field(default=1, description='Top K')

@func.set_output
class Outputs(CoreModel):
    answer: list[str] = Field(..., description='Generated answer')
    score: list[float] = Field(..., description='Confidence score')
