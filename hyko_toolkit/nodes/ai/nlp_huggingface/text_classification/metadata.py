from hyko_sdk.components.components import Search, TextField
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.callbacks_utils.huggingface_utils import huggingface_models_search

node = ToolkitNode(
    name="Text classification",
    cost=0,
    icon="hf",
    description="Hugging Face text classification",
    require_worker=True,
)


@node.set_input
class Inputs(CoreModel):
    input_text: list[str] = field(
        description="Text to classify.",
        component=TextField(placeholder="Enter your text here", multiline=True),
    )


@node.set_param
class Params(CoreModel):
    hugging_face_model: str = field(
        description="Model",
        component=Search(placeholder="Search text classification model"),
    )
    device_map: str = field(description="Device map (Auto, CPU or GPU)")


@node.set_output
class Outputs(CoreModel):
    label: list[str] = field(description="Class labels")
    score: list[float] = field(description="Associated score to the class label")


node.callback(trigger="hugging_face_model", id="hugging_face_search")(
    huggingface_models_search
)
