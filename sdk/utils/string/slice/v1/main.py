from fastapi.exceptions import HTTPException
from metadata import Inputs, Outputs, Params, func


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    text = inputs.text
    start = params.start
    length = params.length
    if length < 0:
        raise HTTPException(status_code=500, detail="Length must not be less than 0")
    start = max(-len(text), start)
    result = text[start : start + length]

    return Outputs(output_text=result)
