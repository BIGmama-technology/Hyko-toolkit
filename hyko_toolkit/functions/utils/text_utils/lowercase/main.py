from hyko_sdk.models import CoreModel
from metadata import Inputs, Outputs, func


@func.on_execute
async def main(inputs: Inputs, params: CoreModel) -> Outputs:
    lowercase_string = inputs.text.lower()
    return Outputs(lowercase_string=lowercase_string)
