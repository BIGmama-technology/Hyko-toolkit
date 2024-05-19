from hyko_sdk.components.components import Search
from hyko_sdk.io import Image
from hyko_sdk.models import CoreModel, ModelMetaData
from hyko_sdk.utils import field
from pydantic import Field

from hyko_toolkit.callbacks_utils import huggingface_models_search
from hyko_toolkit.registry import ToolkitModel

func = ToolkitModel(
    name="text_to_image",
    task="multimodal",
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
    device_map: str = Field(..., description="Device map (Auto, CPU or GPU)")


@func.set_input
class Inputs(CoreModel):
    prompt: str = Field(..., description="Input text")
    image: Image = Field(default=None, description="Input Image")
    negative_prompt: str = Field(default=None, description="Input text")


@func.set_param
class Params(CoreModel):
    num_inference_steps: int = Field(
        default=15, description="The number of de-noising steps."
    )
    strength: float = Field(
        default=0.8,
        description="Indicates extent to transform the reference image (between 0 and 1).",
    )
    guidance_scale: float = Field(
        default=7.5, description="Guidance scale influences image-text coherence.(> 1)"
    )


@func.set_output
class Outputs(CoreModel):
    generated_image: Image = Field(..., description="Generated image")


@func.callback(triggers=["hugging_face_model"], id="text_to_image_search")
async def add_search_results(
    metadata: ModelMetaData, access_token: str, refresh_token: str
) -> ModelMetaData:
    return await huggingface_models_search(metadata)
