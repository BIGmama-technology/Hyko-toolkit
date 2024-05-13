from hyko_sdk.components.components import Slider
from hyko_sdk.io import Image
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.registry import ToolkitModel

func = ToolkitModel(
    name="visual_question_answering",
    task="multimodal",
    description="Hugging Face Image-To-Text Task",
    absolute_dockerfile_path="./toolkit/hyko_toolkit/models/multimodal/Dockerfile",
    docker_context="./toolkit/hyko_toolkit/models/multimodal/visual_question_answering",
)


@func.set_startup_params
class StartupParams(CoreModel):
    hugging_face_model: str = field(description="Model")
    device_map: str = field(description="Device map (Auto, CPU or GPU)")


@func.set_input
class Inputs(CoreModel):
    image: Image = field(description="Input image")
    question: str = field(description="Input question")


@func.set_param
class Params(CoreModel):
    top_k: int = field(
        default=2,
        description="Number of top predictions to return (default: 2).",
        component=Slider(leq=1, geq=5, step=1),
    )


@func.set_output
class Outputs(CoreModel):
    answer: list[str] = field(description="Generated answer")
    score: list[float] = field(description="Confidence score")
