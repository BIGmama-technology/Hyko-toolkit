from hyko_sdk.components.components import Slider
from hyko_sdk.io import Image
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.registry import ToolkitModel

func = ToolkitModel(
    name="image_to_text",
    task="multimodal",
    description="Hugging Face Image-To-Text Task",
    absolute_dockerfile_path="./toolkit/hyko_toolkit/models/multimodal/Dockerfile",
    docker_context="./toolkit/hyko_toolkit/models/multimodal/image_to_text",
)


@func.set_startup_params
class StartupParams(CoreModel):
    hugging_face_model: str = field(description="Model")
    device_map: str = field(description="Device map (Auto, CPU or GPU)")


@func.set_input
class Inputs(CoreModel):
    image: Image = field(description="Input image")


@func.set_param
class Params(CoreModel):
    max_new_tokens: int = field(
        default=30, description="Cap newly generated content length"
    )
    top_k: int = field(
        default=2,
        description="Number of top predictions to return (default: 2)",
        component=Slider(leq=0, geq=5, step=1),
    )
    temperature: float = field(
        default=0.5,
        description="Randomness (fluency vs. creativity)",
        component=Slider(leq=0, geq=1, step=0.01),
    )
    top_p: float = field(
        default=0.5,
        description="Focus high-probability words (diversity control)",
        component=Slider(leq=1, geq=5, step=1),
    )


@func.set_output
class Outputs(CoreModel):
    generated_text: str = field(description="Generated text")
