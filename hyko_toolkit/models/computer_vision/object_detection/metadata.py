from pydantic import Field

from hyko_sdk.definitions import ToolkitModel
from hyko_sdk.io import Image
from hyko_sdk.metadata import CoreModel

func = ToolkitModel(
    name="object_detection",
    task="computer_vision",
    description="Hugging face object detection",
)


@func.set_startup_params
class StartupParams(CoreModel):
    hugging_face_model: str = Field(..., description="Model Id.")
    device_map: str = Field(..., description="Device map (Auto, CPU or GPU).")


@func.set_input
class Inputs(CoreModel):
    input_image: Image = Field(..., description="Input image.")


@func.set_param
class Params(CoreModel):
    threshold: float = Field(
        default=0.7, description="The probability necessary to make a prediction."
    )


@func.set_output
class Outputs(CoreModel):
    final: Image = Field(..., description="Labeled image.")
