from hyko_sdk.io import Audio
from hyko_sdk.models import CoreModel
from pydantic import Field

from hyko_toolkit.registry import ToolkitModel

func = ToolkitModel(name='automatic_speech_recognition', task='audio', description='HuggingFace automatic speech recognition', absolute_dockerfile_path='./toolkit/hyko_toolkit/models/audio/automatic_speech_recognition/Dockerfile', docker_context='./toolkit/hyko_toolkit/models/audio/automatic_speech_recognition')

@func.set_startup_params
class StartupParams(CoreModel):
    hugging_face_model: str = Field(..., description='Model')
    device_map: str = Field(..., description='Device map (Auto, CPU or GPU)')

@func.set_input
class Inputs(CoreModel):
    speech: Audio = Field(..., description='Input speech')

@func.set_param
class Params(CoreModel):
    top_k: int = Field(default=1, description='Keep best k options (exploration vs. fluency)')
    temperature: float = Field(default=0.5, description='Randomness (fluency vs. creativity)')
    top_p: float = Field(default=0.5, description='Focus high-probability words (diversity control)')

@func.set_output
class Outputs(CoreModel):
    text: str = Field(..., description='Recognized speech text')
