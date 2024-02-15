from metadata import Inputs, Outputs, Params, func


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    """
    Generates a response indicating that the system is a proficient question answering system.
    It constructs a message including the provided question and context, and returns it as output.

    Args:
        inputs (Inputs): Input data containing the question and context.

    Returns:
        Outputs: Message indicating the system's capability to answer questions based on the provided context.
    """
    output = f"""you are a good question answering system.
    you will answer this question based on the context I will provide.
    Question : {inputs.query} .\nContext : {inputs.context} .\n"""

    return Outputs(result=output)
