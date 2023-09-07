from fastapi.exceptions import HTTPException
from pydantic import Field
from hyko_sdk import CoreModel, SDKFunction


func = SDKFunction(
    description="Create a slice of a given string of text",
    requires_gpu=False,
)


class Inputs(CoreModel):
    text: str = Field(..., description="Text to be sliced")

class Params(CoreModel):
   
    start: int = Field(default=None, description="Starting position for slicing")
    length: int = Field(default=None, description="Length of the slice")
    
class Outputs(CoreModel):
    output_text: str = Field(..., description="Text slice result")


@func.on_execute
async def main(inputs: Inputs , params: Params)-> Outputs:
    text = inputs.text
    start = params.start
    length = params.length
    if length < 0 :
        raise HTTPException(
            status_code=500,
            detail="Length must not be less than 0"
        )
    start = max(-len(text), start)
    result = text[start: start + length]
   

    return Outputs(output_text=result)
