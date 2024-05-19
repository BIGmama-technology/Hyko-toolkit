from hyko_sdk.components.components import ListComponent, Search, TextField
from hyko_sdk.models import CoreModel, ModelMetaData
from hyko_sdk.utils import field

from hyko_toolkit.callbacks_utils import huggingface_models_search
from hyko_toolkit.registry import ToolkitModel

func = ToolkitModel(
    name="zero-shot-classification",
    task="natural_language_processing",
    cost=0,
    description="Hugging Face Zero Shot Classification Task",
    absolute_dockerfile_path="./toolkit/hyko_toolkit/models/natural_language_processing/Dockerfile",
    docker_context="./toolkit/hyko_toolkit/models/natural_language_processing/zero_shot_classification",
)


@func.set_startup_params
class StartupParams(CoreModel):
    hugging_face_model: str = field(
        description="Model",
        component=Search(placeholder="Search zero shot classification model"),
    )
    device_map: str = field(description="Device map (Auto, CPU or GPU)")


@func.set_input
class Inputs(CoreModel):
    input_text: str = field(
        description="Input text",
        component=TextField(placeholder="Enter your text here", multiline=True),
    )
    candidate_labels: list[str] = field(
        description="Candidate labels to use for classification",
        component=ListComponent(
            item_component=TextField(placeholder="Enter your text here", multiline=True)
        ),
    )


@func.set_output
class Outputs(CoreModel):
    labels: list[str] = field(description="Classified labels")
    scores: list[float] = field(description="Respective classification scores")


@func.callback(triggers=["hugging_face_model"], id="zero_shot_classification_search")
async def add_search_results(
    metadata: ModelMetaData, access_token: str, refresh_token: str
) -> ModelMetaData:
    return await huggingface_models_search(metadata)
