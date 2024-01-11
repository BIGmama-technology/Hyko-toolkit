from fastapi import HTTPException
from metadata import Inputs, Outputs, Params, ReplaceMode, func


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    if params.replace_mode == ReplaceMode.replace_all:
        replaced_text = inputs.text.replace(params.old_substring, params.new_substring)
    elif params.replace_mode == ReplaceMode.replace_first:
        replaced_text = inputs.text.replace(
            params.old_substring, params.new_substring, 1
        )
    else:
        raise HTTPException(
            status_code=500, detail=f"Invalid relace mode'{params.replace_mode}'."
        )

    return Outputs(replaced=replaced_text)
