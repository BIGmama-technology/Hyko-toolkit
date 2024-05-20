from hyko_sdk.components.components import Search, Slider
from hyko_sdk.io import Image
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.callbacks_utils import huggingface_models_search
from hyko_toolkit.registry import ToolkitModel

func = ToolkitModel(
    name="text-to-image",
    task="multimodal",
    cost=0,
    description="Hugging Face Text to Image Task",
    absolute_dockerfile_path="./toolkit/hyko_toolkit/models/multimodal/text_to_image/Dockerfile",
    docker_context="./toolkit/hyko_toolkit/models/multimodal/text_to_image",
)


@func.set_startup_params
class StartupParams(CoreModel):
    hugging_face_model: str = field(
        description="Model",
        component=Search(placeholder="Search text to image model"),
    )
    device_map: str = field(description="Device map (Auto, CPU or GPU)")


@func.set_input
class Inputs(CoreModel):
    prompt: str = field(description="Input text")
    image: Image = field(default=None, description="Input Image")
    negative_prompt: str = field(default=None, description="Input text")


@func.set_param
class Params(CoreModel):
    num_inference_steps: int = field(
        default=16,
        description="The number of de-noising steps.",
        component=Slider(leq=128, geq=16, step=8),
    )
    strength: float = field(
        default=0.8,
        description="Indicates extent to transform the reference image (between 0 and 1).",
        component=Slider(leq=1, geq=0, step=0.01),
    )
    guidance_scale: float = field(
        default=7.5, description="Guidance scale influences image-text coherence.(> 1)"
    )


@func.set_output
class Outputs(CoreModel):
    generated_image: Image = field(description="Generated image")


func.callback(triggers=["hugging_face_model"], id="hugging_face_search")(
    huggingface_models_search
)
