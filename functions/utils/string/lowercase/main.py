from metadata import Inputs, Outputs, Params, func


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    lowercase_string = inputs.text.lower()
    return Outputs(lowercase_string=lowercase_string)
