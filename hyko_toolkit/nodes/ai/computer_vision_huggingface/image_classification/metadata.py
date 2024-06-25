from hyko_sdk.components.components import Search, Slider
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.io import Image
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.callbacks_utils.huggingface_utils import huggingface_models_search

node = ToolkitNode(
    name="Image classification",
    cost=0,
    icon="hf",
    description="HuggingFace image classification",
    require_worker=True,
)


@node.set_param
class Params(CoreModel):
    hugging_face_model: str = field(
        description="Model",
        component=Search(placeholder="Search image classification model"),
    )
    device_map: str = field(description="Device map (Auto, CPU or GPU)")
    top_k: int = field(
        default=2,
        description="Number of top predictions to return (default: 2).",
        component=Slider(leq=5, geq=0, step=1),
    )


@node.set_input
class Inputs(CoreModel):
    input_image: Image = field(description="Input image")


@node.set_output
class Outputs(CoreModel):
    labels: list[str] = field(description="Class of the image.")
    scores: list[float] = field(description="Scores.")


node.callback(trigger="hugging_face_model", id="hugging_face_search")(
    huggingface_models_search
)
