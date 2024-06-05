from hyko_sdk.components.components import Search, Slider, TextField
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.callbacks_utils.huggingface_utils import huggingface_models_search

func = ToolkitNode(
    name="Summarization",
    cost=0,
    icon="hf",
    description="Hugging Face summarization",
)


@func.set_input
class Inputs(CoreModel):
    input_text: str = field(
        description="text to summarize",
        component=TextField(placeholder="Enter your text here", multiline=True),
    )


@func.set_param
class Params(CoreModel):
    hugging_face_model: str = field(
        description="Model",
        component=Search(placeholder="Search summarization model"),
    )
    device_map: str = field(description="Device map (Auto, CPU or GPU)")
    max_length: int = field(default=128, description="Maximum output length")
    min_length: int = field(default=16, description="Minumum output length")
    top_k: int = field(
        default=2,
        description="Number of top predictions to return (default: 2).",
        component=Slider(leq=5, geq=0, step=1),
    )
    temperature: float = field(
        default=0.5, description="Randomness (fluency vs. creativity)"
    )
    top_p: float = field(
        default=0.5,
        description="Focus high-probability words (diversity control)",
        component=Slider(leq=1, geq=0, step=0.01),
    )


@func.set_output
class Outputs(CoreModel):
    summary_text: str = field(description="Summary output")


func.callback(trigger="hugging_face_model", id="hugging_face_search")(
    huggingface_models_search
)
