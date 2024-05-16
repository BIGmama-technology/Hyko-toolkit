from hyko_sdk.components.components import Slider
from hyko_sdk.io import Image
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.registry import ToolkitModel

func = ToolkitModel(
    name="object_detection",
    task="computer_vision",
    cost=0,
    description="Hugging face object detection",
    absolute_dockerfile_path="./toolkit/hyko_toolkit/models/computer_vision/huggingface/object_detection/Dockerfile",
    docker_context="./toolkit/hyko_toolkit/models/computer_vision/huggingface/object_detection",
)


@func.set_startup_params
class StartupParams(CoreModel):
    hugging_face_model: str = field(description="Model Id.")
    device_map: str = field(description="Device map (Auto, CPU or GPU).")


@func.set_input
class Inputs(CoreModel):
    input_image: Image = field(description="Input image.")


@func.set_param
class Params(CoreModel):
    threshold: float = field(
        default=0.7,
        description="The probability necessary to make a prediction.",
        component=Slider(leq=1, geq=0, step=0.01),
    )


@func.set_output
class Outputs(CoreModel):
    final: Image = field(description="Labeled image.")
