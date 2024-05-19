from hyko_sdk.components.components import Search
from hyko_sdk.models import CoreModel, ModelMetaData
from hyko_sdk.utils import field
from pydantic import Field

from hyko_toolkit.callbacks_utils import huggingface_models_search
from hyko_toolkit.registry import ToolkitModel

func = ToolkitModel(
    name="text-generation",
    task="natural_language_processing",
    description="Hugging Face text generation",
    absolute_dockerfile_path="./toolkit/hyko_toolkit/models/natural_language_processing/Dockerfile",
    docker_context="./toolkit/hyko_toolkit/models/natural_language_processing/text_generation",
)


@func.set_startup_params
class StartupParams(CoreModel):
    hugging_face_model: str = field(
        description="Model",
        component=Search(placeholder="Search text generation model"),
    )
    device_map: str = Field(..., description="Device map (Auto, CPU or GPU)")


@func.set_input
class Inputs(CoreModel):
    input_text: str = Field(..., description="input text")


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
    generated_text: str = Field(..., description="Completion text")


@func.callback(triggers=["hugging_face_model"], id="text_generation_search")
async def add_search_results(
    metadata: ModelMetaData, access_token: str, refresh_token: str
) -> ModelMetaData:
    return await huggingface_models_search(metadata)
