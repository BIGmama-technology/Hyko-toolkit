from pydantic import Field

from hyko_sdk.function import SDKFunction
from hyko_sdk.io import Image
from hyko_sdk.metadata import CoreModel

func = SDKFunction(
    description="Object detection/recogntion model, draws bounding boxes over the image if the object is in the list of tags.",
)


@func.set_input
class Inputs(CoreModel):
    img: Image = Field(..., description="Input Image")
    tags: list[str] = Field(..., description="List of object(s) names to be detected")


@func.set_param
class Params(CoreModel):
    pass


@func.set_output
class Outputs(CoreModel):
    output_image: Image = Field(
        ..., description="Input image + detection bounding Boxes"
    )
