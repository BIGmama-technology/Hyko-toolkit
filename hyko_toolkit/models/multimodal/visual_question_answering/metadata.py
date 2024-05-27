from hyko_sdk.components.components import Slider
from hyko_sdk.io import Image
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.registry import ToolkitModel

func = ToolkitModel(
    name="visual_question_answering",
    task="multimodal",
    cost=0,
    description="Hugging Face Image-To-Text Task",
)


@func.set_input
class Inputs(CoreModel):
    image: Image = field(description="Input image")
    question: str = field(description="Input question")


@func.set_param
class Params(CoreModel):
    hugging_face_model: str = field(description="Model")
    device_map: str = field(description="Device map (Auto, CPU or GPU)")
    top_k: int = field(
        default=2,
        description="Number of top predictions to return (default: 2).",
        component=Slider(leq=5, geq=1, step=1),
    )


@func.set_output
class Outputs(CoreModel):
    answer: list[str] = field(description="Generated answer")
    score: list[float] = field(description="Confidence score")
