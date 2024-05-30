from hyko_sdk.components.components import Search, TextField
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.callbacks_utils import huggingface_models_search
from hyko_toolkit.registry import ToolkitModel

func = ToolkitModel(
    name="Text classification",
    task="Natural language processing",
    cost=0,
    icon="hf",
    description="Hugging Face text classification",
)


@func.set_input
class Inputs(CoreModel):
    input_text: list[str] = field(
        description="Text to classify.",
        component=TextField(placeholder="Enter your text here", multiline=True),
    )


@func.set_param
class Params(CoreModel):
    hugging_face_model: str = field(
        description="Model",
        component=Search(placeholder="Search text classification model"),
    )
    device_map: str = field(description="Device map (Auto, CPU or GPU)")


@func.set_output
class Outputs(CoreModel):
    label: list[str] = field(description="Class labels")
    score: list[float] = field(description="Associated score to the class label")


func.callback(triggers=["hugging_face_model"], id="hugging_face_search")(
    huggingface_models_search
)
