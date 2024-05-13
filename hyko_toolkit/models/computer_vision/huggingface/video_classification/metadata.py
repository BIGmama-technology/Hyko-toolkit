from hyko_sdk.components.components import Slider
from hyko_sdk.io import Video
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.registry import ToolkitModel

func = ToolkitModel(
    name="video_classification",
    task="computer_vision",
    description="HuggingFace video classification",
    absolute_dockerfile_path="./toolkit/hyko_toolkit/models/computer_vision/huggingface/video_classification/Dockerfile",
    docker_context="./toolkit/hyko_toolkit/models/computer_vision/huggingface/video_classification",
)


@func.set_startup_params
class StartupParams(CoreModel):
    hugging_face_model: str = field(description="Model")
    device_map: str = field(description="Device map (Auto, CPU or GPU)")


@func.set_input
class Inputs(CoreModel):
    input_video: Video = field(description="Input image")


@func.set_param
class Params(CoreModel):
    top_k: int = field(
        default=1,
        description="The number of top labels that will be returned by the pipeline.",
        component=Slider(leq=0, geq=5, step=1),
    )
    frame_sampling_rate: int = field(
        default=1, description="The sampling rate used to select frames from the video."
    )


@func.set_output
class Outputs(CoreModel):
    labels: list[str] = field(description="Class of the video.")
    scores: list[float] = field(description="Scores for each class.")
