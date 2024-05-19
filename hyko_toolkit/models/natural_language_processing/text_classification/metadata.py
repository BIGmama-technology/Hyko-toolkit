from hyko_sdk.components.components import Search
from hyko_sdk.models import CoreModel, ModelMetaData
from hyko_sdk.utils import field
from pydantic import Field

from hyko_toolkit.callbacks_utils import huggingface_models_search
from hyko_toolkit.registry import ToolkitModel

func = ToolkitModel(
    name="text_classification",
    task="natural_language_processing",
    description="Hugging Face text classification",
    absolute_dockerfile_path="./toolkit/hyko_toolkit/models/natural_language_processing/Dockerfile",
    docker_context="./toolkit/hyko_toolkit/models/natural_language_processing/text_classification",
)


@func.set_startup_params
class StartupParams(CoreModel):
    hugging_face_model: str = field(
        description="Model",
        component=Search(placeholder="Search text classification model"),
    )
    device_map: str = Field(..., description="Device map (Auto, CPU or GPU)")


@func.set_input
class Inputs(CoreModel):
    input_text: list[str] = Field(..., description="Text to classify.")


@func.set_output
class Outputs(CoreModel):
    label: list[str] = Field(..., description="Class labels")
    score: list[float] = Field(..., description="Associated score to the class label")


@func.callback(triggers=["hugging_face_model"], id="text_classification_search")
async def add_search_results(
    metadata: ModelMetaData, access_token: str, refresh_token: str
) -> ModelMetaData:
    return await huggingface_models_search(metadata)
