from hyko_sdk.components.components import Slider
from hyko_sdk.io import Audio
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.registry import ToolkitModel

func = ToolkitModel(
    name="automatic_speech_recognition",
    task="audio",
    cost=0,
    description="HuggingFace automatic speech recognition",
    absolute_dockerfile_path="./toolkit/hyko_toolkit/models/audio/automatic_speech_recognition/Dockerfile",
    docker_context="./toolkit/hyko_toolkit/models/audio/automatic_speech_recognition",
)


@func.set_startup_params
class StartupParams(CoreModel):
    hugging_face_model: str = field(description="Model")
    device_map: str = field(description="Device map (Auto, CPU or GPU)")


@func.set_input
class Inputs(CoreModel):
    speech: Audio = field(description="Input speech")


@func.set_param
class Params(CoreModel):
    top_k: int = field(
        default=2,
        description="Number of top predictions to return (default: 2).",
        component=Slider(leq=5, geq=0, step=1),
    )
    temperature: float = field(
        default=0.5,
        description="Randomness (fluency vs. creativity)",
        component=Slider(leq=1, geq=0, step=0.01),
    )
    top_p: float = field(
        default=0.5,
        description="Focus high-probability words (diversity control)",
        component=Slider(leq=1, geq=0, step=0.01),
    )


@func.set_output
class Outputs(CoreModel):
    text: str = field(description="Recognized speech text")
