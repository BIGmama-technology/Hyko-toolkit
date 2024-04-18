from hyko_sdk.models import CoreModel
from pydantic import Field

from hyko_toolkit.registry import ToolkitModel

func = ToolkitModel(name='fill_mask', task='natural_language_processing', description='Hugging Face fill mask task', absolute_dockerfile_path='./toolkit/hyko_toolkit/models/natural_language_processing/Dockerfile', docker_context='./toolkit/hyko_toolkit/models/natural_language_processing/fill_mask')

@func.set_startup_params
class StartupParams(CoreModel):
    hugging_face_model: str = Field(..., description='Model')
    device_map: str = Field(..., description='Device map (Auto, CPU or GPU)')

@func.set_input
class Inputs(CoreModel):
    masked_text: str = Field(..., description='Input text with <mask> to fill')

@func.set_param
class Params(CoreModel):
    top_k: int = Field(default=5, description='Number of top predictions to return (default: 5).')

@func.set_output
class Outputs(CoreModel):
    sequence: list[str] = Field(..., description='Filled output text')
    score: list[float] = Field(..., description='Score of the filled sequence')
