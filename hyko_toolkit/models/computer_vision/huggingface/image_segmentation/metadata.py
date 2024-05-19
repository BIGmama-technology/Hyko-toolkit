from hyko_sdk.components.components import Search, Slider
from hyko_sdk.io import Image
from hyko_sdk.models import CoreModel, ModelMetaData
from hyko_sdk.utils import field

from hyko_toolkit.callbacks_utils import huggingface_models_search
from hyko_toolkit.registry import ToolkitModel

func = ToolkitModel(
    name="image-segmentation",
    task="computer_vision",
    cost=0,
    description="HuggingFace image segmentation",
    absolute_dockerfile_path="./toolkit/hyko_toolkit/models/computer_vision/huggingface/Dockerfile",
    docker_context="./toolkit/hyko_toolkit/models/computer_vision/huggingface/image_segmentation",
)


@func.set_startup_params
class StartupParams(CoreModel):
    hugging_face_model: str = field(
        description="Model",
        component=Search(placeholder="Search image segmentation model"),
    )
    device_map: str = field(description="Device map (Auto, CPU or GPU)")


@func.set_input
class Inputs(CoreModel):
    input_image: Image = field(description="Input image")


@func.set_param
class Params(CoreModel):
    threshold: float = field(
        default=0.9,
        description="Probability threshold to filter out predicted masks.",
        component=Slider(leq=1, geq=0, step=0.01),
    )
    mask_threshold: float = field(
        default=0.5,
        description="Threshold to use when turning the predicted masks into binary values.",
        component=Slider(leq=1, geq=0, step=0.01),
    )
    overlap_mask_area_threshold: float = field(
        default=0.5,
        description="Mask overlap threshold to eliminate small, disconnected segments.",
        component=Slider(leq=1, geq=0, step=0.01),
    )


@func.set_output
class Outputs(CoreModel):
    mask: Image = field(description="Segmented image")


@func.callback(triggers=["hugging_face_model"], id="image_segmentation_search")
async def add_search_results(
    metadata: ModelMetaData, access_token: str, refresh_token: str
) -> ModelMetaData:
    return await huggingface_models_search(metadata)
