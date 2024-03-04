from pydantic import Field

from hyko_sdk.function import SDKFunction
from hyko_sdk.io import Image
from hyko_sdk.metadata import CoreModel

func = SDKFunction(
    description="HuggingFace image segmentation",
)


@func.set_startup_params
class StartupParams(CoreModel):
    hugging_face_model: str = Field(..., description="Model")
    device_map: str = Field(..., description="Device map (Auto, CPU or GPU)")


@func.set_input
class Inputs(CoreModel):
    input_image: Image = Field(..., description="Input image")


@func.set_param
class Params(CoreModel):
    threshold: float = Field(
        default=0.9, description="Probability threshold to filter out predicted masks."
    )
    mask_threshold: float = Field(
        default=0.5,
        description="Threshold to use when turning the predicted masks into binary values.",
    )
    overlap_mask_area_threshold: float = Field(
        default=0.5,
        description="Mask overlap threshold to eliminate small, disconnected segments.",
    )


@func.set_output
class Outputs(CoreModel):
    mask: Image = Field(..., description="Segmented image")
