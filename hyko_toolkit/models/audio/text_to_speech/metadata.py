from hyko_sdk.components.components import Search, Slider
from hyko_sdk.io import Audio
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.callbacks_utils import huggingface_models_search
from hyko_toolkit.registry import ToolkitModel

func = ToolkitModel(
    name="Text to speech",
    task="Audio",
    cost=0,
    icon="hf",
    description="HuggingFace text to speech, run on cuda may cause issues on cpu",
    absolute_dockerfile_path="./toolkit/hyko_toolkit/models/audio/text_to_speech/Dockerfile",
    docker_context="./toolkit/hyko_toolkit/models/audio/text_to_speech",
)


@func.set_param
class StartupParams(CoreModel):
    hugging_face_model: str = field(
        description="Model",
        component=Search(placeholder="Search Text to speech model"),
    )
    device_map: str = field(description="Device map (Auto, CPU or GPU)")
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


@func.set_input
class Inputs(CoreModel):
    text: str = field(description="Input text")


@func.set_output
class Outputs(CoreModel):
    speech: Audio = field(description="Synthesized speech")


func.callback(triggers=["hugging_face_model"], id="hugging_face_search")(
    huggingface_models_search
)
