from pydantic import Field
from hyko_sdk import CoreModel, extract_metadata, Image
from typing import List

description = "Object detection/recogntion model, draws bounding boxes over the image if the object is in the list of tags."

class Inputs(CoreModel):
    img : Image = Field(..., description="Input Image")

class Params(CoreModel):
    tags : List[str] = Field(..., description="List of object(s) names to be detected")

class Outputs(CoreModel):
    output_image: Image = Field(..., description="Input image + detection bounding Boxes")
    
if __name__ == "__main__":
    extract_metadata(
                    Inputs, Params, Outputs,  # type: ignore
                    description, False
                )