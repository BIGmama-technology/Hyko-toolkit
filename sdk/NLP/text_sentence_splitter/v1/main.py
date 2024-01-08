import nltk
from pydantic import Field

from hyko_sdk.function import SDKFunction
from hyko_sdk.metadata import CoreModel

func = SDKFunction(
    description="Takes a paragraph and tokenizes (splits) it into a list of sentences",
    requires_gpu=False,
)


@func.on_startup
async def init():
    nltk.download("punkt")


class Inputs(CoreModel):
    text: str = Field(..., description="Text to be split")


class Params(CoreModel):
    pass


class Outputs(CoreModel):
    sentences: list[str] = Field(..., description="Splitted sentences")


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    return Outputs(sentences=nltk.sent_tokenize(inputs.text))
