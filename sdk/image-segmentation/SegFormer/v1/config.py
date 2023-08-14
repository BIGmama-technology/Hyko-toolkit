from pydantic import Field
from hyko_sdk import Image, CoreModel, extract_metadata

description = "Image Segmentation Model, this models takes an image and partition it to locate objects and their contours in the image"

class Inputs(CoreModel):
    image : Image = Field(..., description="User inputted image to be segmented")

class Params(CoreModel):
    pass

class Outputs(CoreModel):
    segmented_image : Image = Field(..., description="Segmented image")

if __name__ == "__main__":
    extract_metadata(
                    Inputs, Params, Outputs,  # type: ignore
                    description, False
                )