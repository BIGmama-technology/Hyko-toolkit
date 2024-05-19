from hyko_sdk.components.components import Search
from hyko_sdk.io import Image
from hyko_sdk.models import CoreModel, ModelMetaData
from hyko_sdk.utils import field
from pydantic import Field

from hyko_toolkit.callbacks_utils import huggingface_models_search
from hyko_toolkit.registry import ToolkitModel

func = ToolkitModel(
    name="image-to-text",
    task="multimodal",
    description="Hugging Face Image-To-Text Task",
    absolute_dockerfile_path="./toolkit/hyko_toolkit/models/multimodal/Dockerfile",
    docker_context="./toolkit/hyko_toolkit/models/multimodal/image_to_text",
)


@func.set_startup_params
class StartupParams(CoreModel):
    hugging_face_model: str = field(
        description="Model",
        component=Search(placeholder="Search image to text model"),
    )
    device_map: str = Field(..., description="Device map (Auto, CPU or GPU)")


@func.set_input
class Inputs(CoreModel):
    image: Image = Field(..., description="Input image")


@func.set_param
class Params(CoreModel):
    max_new_tokens: int = Field(
        default=30, description="Cap newly generated content length"
    )
    top_k: int = Field(
        default=1, description="Keep best k options (exploration vs. fluency)"
    )
    temperature: float = Field(
        default=0.5, description="Randomness (fluency vs. creativity)"
    )
    top_p: float = Field(
        default=0.5, description="Focus high-probability words (diversity control)"
    )


@func.set_output
class Outputs(CoreModel):
    generated_text: str = Field(..., description="Generated text")


@func.callback(triggers=["hugging_face_model"], id="image_to_text_search")
async def add_search_results(
    metadata: ModelMetaData, access_token: str, refresh_token: str
) -> ModelMetaData:
    return await huggingface_models_search(metadata)
