from fastapi import HTTPException
from metadata import Inputs, Outputs, PaddingAlignment, Params, func


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    text = inputs.text
    width = params.width
    padding = params.padding
    alignment = params.alignment

    if alignment == PaddingAlignment.START:
        result = text.rjust(width, padding)
    elif alignment == PaddingAlignment.END:
        result = text.ljust(width, padding)
    elif alignment == PaddingAlignment.CENTER:
        result = text.center(width, padding)
    else:
        raise HTTPException(status_code=500, detail=f"Invalid alignment '{alignment}'.")

    return Outputs(output_text=result)
