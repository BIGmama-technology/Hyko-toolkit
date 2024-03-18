from hyko_sdk.models import CoreModel
from metadata import Inputs, Outputs, func


@func.on_execute
async def main(inputs: Inputs, params: CoreModel) -> Outputs:
    return Outputs(output=inputs.first + inputs.second)
