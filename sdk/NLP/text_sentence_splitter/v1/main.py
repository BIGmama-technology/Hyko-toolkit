from hyko_sdk import SDKFunction, CoreModel
from pydantic import Field
import nltk


func = SDKFunction(
    description="Takes a paragraph and tokenizes (splits) it into a list of sentences",
    requires_gpu=False,
)


@func.on_startup
async def init():
    nltk.download('punkt')


class Inputs(CoreModel):
    text: str = Field(..., description="Text to be split")

class Params(CoreModel):
    pass

class Outputs(CoreModel):
    sentences: list[str] = Field(..., descriptions="Splitted sentences")


@func.on_execute
async def main(inputs: Inputs, params : Params):
    return Outputs(sentences=nltk.sent_tokenize(inputs.text))
