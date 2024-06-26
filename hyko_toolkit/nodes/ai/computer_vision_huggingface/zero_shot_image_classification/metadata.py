from hyko_sdk.components.components import Search
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.io import Image
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.callbacks_utils.huggingface_utils import huggingface_models_search

node = ToolkitNode(
    name="Zero shot image classification",
    cost=0,
    icon="hf",
    description="Hugging Face image classification",
    require_worker=True,
)


@node.set_input
class Inputs(CoreModel):
    input_image: Image = field(description="Input image")
    labels: list[str] = field(description="Labels for classification")


@node.set_param
class Params(CoreModel):
    hugging_face_model: str = field(
        description="Model",
        component=Search(placeholder="Search zero shot image classification model"),
    )
    device_map: str = field(description="Device map (Auto, CPU or GPU)")
    hypothesis_template: str = field(
        default="This is a photo of {}",
        description="Template for image classification hypothesis.",
    )


@node.set_output
class Outputs(CoreModel):
    labels: list[str] = field(description="Class of the image.")
    scores: list[float] = field(description="Scores for each class.")


node.callback(trigger="hugging_face_model", id="hugging_face_search")(
    huggingface_models_search
)
