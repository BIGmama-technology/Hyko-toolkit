from hyko_sdk.components.components import Search, Slider
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.io import Video
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.callbacks_utils.huggingface_utils import huggingface_models_search

func = ToolkitNode(
    name="Video classification",
    cost=0,
    icon="hf",
    description="HuggingFace video classification",
)


@func.set_param
class Params(CoreModel):
    hugging_face_model: str = field(
        description="Model",
        component=Search(placeholder="Search video classification model"),
    )
    device_map: str = field(description="Device map (Auto, CPU or GPU)")
    top_k: int = field(
        default=1,
        description="The number of top labels that will be returned by the pipeline.",
        component=Slider(leq=5, geq=0, step=1),
    )
    frame_sampling_rate: int = field(
        default=1, description="The sampling rate used to select frames from the video."
    )


@func.set_input
class Inputs(CoreModel):
    input_video: Video = field(description="Input image")


@func.set_output
class Outputs(CoreModel):
    labels: list[str] = field(description="Class of the video.")
    scores: list[float] = field(description="Scores for each class.")


func.callback(trigger="hugging_face_model", id="hugging_face_search")(
    huggingface_models_search
)
