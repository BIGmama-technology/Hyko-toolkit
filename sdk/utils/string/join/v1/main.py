from metadata import Inputs, Outputs, Params, func


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    return Outputs(joined_string=params.delimiter.join(inputs.strings))
