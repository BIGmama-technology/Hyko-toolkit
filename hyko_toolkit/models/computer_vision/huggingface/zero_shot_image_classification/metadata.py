from hyko_sdk.components.components import Search
from hyko_sdk.io import Image
from hyko_sdk.models import Category, CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.callbacks_utils.huggingface_utils import huggingface_models_search
from hyko_toolkit.registry import ToolkitNode

func = ToolkitNode(
    name="Zero shot image classification",
    task="Computer vision",
    cost=0,
    icon="hf",
    description="Hugging Face image classification",
    category=Category.MODEL,
)


@func.set_input
class Inputs(CoreModel):
    input_image: Image = field(description="Input image")
    labels: list[str] = field(description="Labels for classification")


@func.set_param
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


@func.set_output
class Outputs(CoreModel):
    labels: list[str] = field(description="Class of the image.")
    scores: list[float] = field(description="Scores for each class.")


func.callback(triggers=["hugging_face_model"], id="hugging_face_search")(
    huggingface_models_search
)
