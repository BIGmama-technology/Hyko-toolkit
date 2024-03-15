from hyko_sdk.definitions import ToolkitModel
from hyko_sdk.io import Image
from hyko_sdk.models import CoreModel
from pydantic import Field

func = ToolkitModel(
    name="mask_generation",
    task="computer_vision",
    description="HuggingFace mask generation.",
)


@func.set_startup_params
class StartupParams(CoreModel):
    hugging_face_model: str = Field(
        default="facebook/sam-vit-base", description="Model"
    )
    device_map: str = Field(default="cpu", description="Device map (Auto, CPU or GPU)")


@func.set_param
class Params(CoreModel):
    mask_threshold: float = Field(
        default=0.0,
        description="Threshold to use when turning the predicted masks into binary values.",
    )
    points_per_batch: int = Field(
        default=128,
        description="Sets the number of points run simultaneously by the model.",
    )
    pred_iou_thresh: float = Field(
        default=0.95,
        description="A filtering threshold in [0,1] applied on the model's predicted mask quality.",
    )


@func.set_input
class Inputs(CoreModel):
    input_image: Image = Field(..., description="Input image")


@func.set_output
class Outputs(CoreModel):
    bbox_img: Image = Field(..., description="Boundig Boxes")
    mask_img: Image = Field(..., description="Maskes")
