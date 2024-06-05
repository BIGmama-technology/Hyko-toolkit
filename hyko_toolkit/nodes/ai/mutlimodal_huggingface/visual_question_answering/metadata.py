from hyko_sdk.components.components import Search, Slider
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.io import Image
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.callbacks_utils.huggingface_utils import huggingface_models_search

func = ToolkitNode(
    name="visual-question-answering",
    cost=0,
    icon="hf",
    description="Hugging Face Image-To-Text Task",
)


@func.set_input
class Inputs(CoreModel):
    image: Image = field(description="Input image")
    question: str = field(description="Input question")


@func.set_param
class Params(CoreModel):
    hugging_face_model: str = field(
        description="Model",
        component=Search(placeholder="Search visual question answering model"),
    )
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


func.callback(trigger="hugging_face_model", id="hugging_face_search")(
    huggingface_models_search
)
