from hyko_sdk.components.components import Search
from hyko_sdk.io import Video
from hyko_sdk.models import CoreModel, ModelMetaData
from hyko_sdk.utils import field
from pydantic import Field

from hyko_toolkit.callbacks_utils import huggingface_models_search
from hyko_toolkit.registry import ToolkitModel

func = ToolkitModel(
    name="video-classification",
    task="computer_vision",
    description="HuggingFace video classification",
    absolute_dockerfile_path="./toolkit/hyko_toolkit/models/computer_vision/huggingface/video_classification/Dockerfile",
    docker_context="./toolkit/hyko_toolkit/models/computer_vision/huggingface/video_classification",
)


@func.set_startup_params
class StartupParams(CoreModel):
    hugging_face_model: str = field(
        description="Model",
        component=Search(placeholder="Search video classification model"),
    )
    device_map: str = Field(..., description="Device map (Auto, CPU or GPU)")


@func.set_input
class Inputs(CoreModel):
    input_video: Video = Field(..., description="Input image")


@func.set_param
class Params(CoreModel):
    top_k: int = Field(
        default=1,
        description="The number of top labels that will be returned by the pipeline.",
    )
    frame_sampling_rate: int = Field(
        default=1, description="The sampling rate used to select frames from the video."
    )


@func.set_output
class Outputs(CoreModel):
    labels: list[str] = Field(..., description="Class of the video.")
    scores: list[float] = Field(..., description="Scores for each class.")


@func.callback(triggers=["hugging_face_model"], id="video_classification_search")
async def add_search_results(
    metadata: ModelMetaData, access_token: str, refresh_token: str
) -> ModelMetaData:
    return await huggingface_models_search(metadata)
