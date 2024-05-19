from hyko_sdk.components.components import Search
from hyko_sdk.models import CoreModel, ModelMetaData
from hyko_sdk.utils import field
from pydantic import Field

from hyko_toolkit.callbacks_utils import huggingface_models_search
from hyko_toolkit.registry import ToolkitModel

func = ToolkitModel(
    name="summarization",
    task="natural_language_processing",
    description="Hugging Face summarization",
    absolute_dockerfile_path="./toolkit/hyko_toolkit/models/natural_language_processing/Dockerfile",
    docker_context="./toolkit/hyko_toolkit/models/natural_language_processing/summarization",
)


@func.set_startup_params
class StartupParams(CoreModel):
    hugging_face_model: str = field(
        description="Model",
        component=Search(placeholder="Search summarization model"),
    )
    device_map: str = Field(..., description="Device map (Auto, CPU or GPU)")


@func.set_input
class Inputs(CoreModel):
    input_text: str = Field(..., description="text to summarize")


@func.set_param
class Params(CoreModel):
    max_length: int = Field(default=130, description="Maximum output length")
    min_length: int = Field(default=0, description="Minumum output length")
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
    summary_text: str = Field(..., description="Summary output")


@func.callback(triggers=["hugging_face_model"], id="summarization_search")
async def add_search_results(
    metadata: ModelMetaData, access_token: str, refresh_token: str
) -> ModelMetaData:
    return await huggingface_models_search(metadata)
