from hyko_sdk.components.components import ListComponent, Search, TextField
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.callbacks_utils.huggingface_utils import huggingface_models_search

func = ToolkitNode(
    name="Zero shot classification",
    cost=0,
    icon="hf",
    description="Hugging Face Zero Shot Classification Task",
)


@func.set_param
class Params(CoreModel):
    hugging_face_model: str = field(
        description="Model",
        component=Search(placeholder="Search zero shot classification model"),
    )
    device_map: str = field(description="Device map (Auto, CPU or GPU)")


@func.set_input
class Inputs(CoreModel):
    input_text: str = field(
        description="Input text",
        component=TextField(placeholder="Enter your text here", multiline=True),
    )
    candidate_labels: list[str] = field(
        description="Candidate labels to use for classification",
        component=ListComponent(
            item_component=TextField(placeholder="Enter your text here", multiline=True)
        ),
    )


@func.set_output
class Outputs(CoreModel):
    labels: list[str] = field(description="Classified labels")
    scores: list[float] = field(description="Respective classification scores")


func.callback(trigger="hugging_face_model", id="hugging_face_search")(
    huggingface_models_search
)
