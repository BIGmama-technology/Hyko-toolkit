import logging
import re

from hyko_sdk.function import SDKFunction
from hyko_sdk.metadata import CoreModel

func = SDKFunction(
    description="Takes a paragraph and tokenizes (splits) it into a list of sentences",
    requires_gpu=False,
)


class Inputs(CoreModel):
    text: str = Field(..., description="Text to be split")


class Params(CoreModel):
    pass


class Outputs(CoreModel):
    sentences: list[str] = Field(..., description="Splitted sentences")


@func.on_startup
async def init():
    return


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    logging.error("input", inputs.text)
    sentences = re.split(r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s", inputs.text)
    logging.error("output", sentences)
    return Outputs(sentences=sentences)
