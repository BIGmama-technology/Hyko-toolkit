from hyko_sdk.definitions import ToolkitModel
from hyko_sdk.io import Video
from hyko_sdk.models import CoreModel
from pydantic import Field

func = ToolkitModel(
    name="video_classification",
    task="computer_vision",
    description="HuggingFace video classification",
)


@func.set_startup_params
class StartupParams(CoreModel):
    hugging_face_model: str = Field(..., description="Model")
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
