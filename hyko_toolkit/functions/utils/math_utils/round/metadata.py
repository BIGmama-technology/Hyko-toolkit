from enum import Enum

from hyko_sdk.models import CoreModel
from pydantic import Field

from hyko_toolkit.registry import ToolkitFunction

func = ToolkitFunction(name='round', task='math_utils', description='Round an input number', absolute_dockerfile_path='./toolkit/hyko_toolkit/functions/utils/math_utils/Dockerfile', docker_context='./toolkit/hyko_toolkit/functions/utils/math_utils/round')

class RoundOperation(str, Enum):
    FLOOR = 'Round down'
    CEILING = 'Round up'
    ROUND = 'Round'

@func.set_input
class Inputs(CoreModel):
    a: float = Field(..., description='Input number')

@func.set_param
class Params(CoreModel):
    operation: RoundOperation = Field(default=RoundOperation.ROUND, description='Rounding operation')

@func.set_output
class Outputs(CoreModel):
    result: float = Field(..., description='Rounded number result')
