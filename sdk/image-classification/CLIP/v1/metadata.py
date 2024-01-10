from pydantic import Field

from hyko_sdk.function import SDKFunction
from hyko_sdk.io import Image
from hyko_sdk.metadata import CoreModel

func = SDKFunction(
    description="""
Classify an image to one class out of the list of classes.
Example: if the classes are ['cat', 'dog'] then the model will have to choose if the image is either a cat or dog
""",
    requires_gpu=False,
)


@func.set_input
class Inputs(CoreModel):
    image: Image = Field(..., description="Image input by user to be classified")


@func.set_param
class Params(CoreModel):
    classes: list[str] = Field(
        ..., description="List of classes to classify the input image on"
    )


@func.set_output
class Outputs(CoreModel):
    output_class: str = Field(..., description="The class of the image")
