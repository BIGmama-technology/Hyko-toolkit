import nltk
from metadata import Inputs, Outputs, Params, func


@func.on_startup
async def init():
    nltk.download("punkt")


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    return Outputs(sentences=nltk.sent_tokenize(inputs.text))
