from metadata import Inputs, Outputs, Params, func


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    output = f"""you are a good question answering system.
    you will answer this question based on the context I will provide.
    Question : {inputs.query} .\nContext : {inputs.context} .\n"""

    return Outputs(result=output)
