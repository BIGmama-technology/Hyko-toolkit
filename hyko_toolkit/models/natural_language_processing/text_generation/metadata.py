from hyko_sdk.components.components import Slider, TextField
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.registry import ToolkitModel

func = ToolkitModel(
    name="text_generation",
    task="natural_language_processing",
    cost=0,
    description="Hugging Face text generation",
)


@func.set_input
class Inputs(CoreModel):
    input_text: str = field(
        description="input text",
        component=TextField(placeholder="Enter your text here", multiline=True),
    )


@func.set_param
class Params(CoreModel):
    hugging_face_model: str = field(description="Model")
    device_map: str = field(description="Device map (Auto, CPU or GPU)")
    max_new_tokens: int = field(
        default=30, description="Cap newly generated content length"
    )
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
    generated_text: str = field(description="Completion text")
