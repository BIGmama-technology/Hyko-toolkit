from hyko_sdk.components.components import Search
from hyko_sdk.models import CoreModel, ModelMetaData
from hyko_sdk.utils import field
from pydantic import Field

from hyko_toolkit.callbacks_utils import huggingface_models_search
from hyko_toolkit.registry import ToolkitModel

func = ToolkitModel(
    name="question_answering",
    task="natural_language_processing",
    description="Hugging Face Question Answering task",
    absolute_dockerfile_path="./toolkit/hyko_toolkit/models/natural_language_processing/Dockerfile",
    docker_context="./toolkit/hyko_toolkit/models/natural_language_processing/question_answering",
)


@func.set_startup_params
class StartupParams(CoreModel):
    hugging_face_model: str = field(
        description="Model",
        component=Search(placeholder="Search question answering model"),
    )
    device_map: str = Field(..., description="Device map (Auto, CPU or GPU)")


@func.set_input
class Inputs(CoreModel):
    question: str = Field(..., description="Input question")
    context: str = Field(..., description="Context from which to answer the question")


@func.set_param
class Params(CoreModel):
    top_k: int = Field(default=1, description="Keep best k options (default:1).")
    doc_stride: int = Field(
        default=1,
        description="The stride of the splitting sliding window (default:128).",
    )


@func.set_output
class Outputs(CoreModel):
    answer: str = Field(..., description="Answer to the question")
    start: int = Field(..., description="Start index")
    end: int = Field(..., description="End index")
    score: float = Field(..., description="Score of the answer")


@func.callback(triggers=["hugging_face_model"], id="question_answering_search")
async def add_search_results(
    metadata: ModelMetaData, access_token: str, refresh_token: str
) -> ModelMetaData:
    return await huggingface_models_search(metadata)
