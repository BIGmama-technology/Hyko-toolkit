from hyko_sdk.components.components import Search, Slider, TextField
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.callbacks_utils.huggingface_utils import huggingface_models_search

node = ToolkitNode(
    name="Fill mask",
    cost=0,
    icon="hf",
    description="Hugging Face fill mask task",
)


@node.set_input
class Inputs(CoreModel):
    masked_text: str = field(
        description="Input text with <mask> to fill",
        component=TextField(placeholder="Enter your text here", multiline=True),
    )


@node.set_param
class Params(CoreModel):
    hugging_face_model: str = field(
        description="Model",
        component=Search(placeholder="Search fill mask model"),
    )
    device_map: str = field(description="Device map (Auto, CPU or GPU)")
    top_k: int = field(
        default=5,
        description="Number of top predictions to return (default: 5).",
        component=Slider(leq=5, geq=1, step=1),
    )


@node.set_output
class Outputs(CoreModel):
    sequence: list[str] = field(description="Filled output text")
    score: list[float] = field(description="Score of the filled sequence")


node.callback(trigger="hugging_face_model", id="hugging_face_search")(
    huggingface_models_search
)
