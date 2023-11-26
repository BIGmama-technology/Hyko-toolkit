from pydantic import Field
from hyko_sdk import CoreModel, SDKFunction

func = SDKFunction(
    description="Count number of words in a text",
    requires_gpu=False,
)

class Inputs(CoreModel):
    text: str = Field(..., description="Input text")

class Params(CoreModel):
    pass

class Outputs(CoreModel):
    count: int = Field(..., description="Number of words")


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    return Outputs(count=len(inputs.text.split(' ')))
