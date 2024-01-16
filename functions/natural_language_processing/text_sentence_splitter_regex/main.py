import logging
import re

from metadata import Inputs, Outputs, Params, func


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    logging.error("input", inputs.text)
    sentences = re.split(r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s", inputs.text)
    logging.error("output", sentences)
    return Outputs(sentences=sentences)
