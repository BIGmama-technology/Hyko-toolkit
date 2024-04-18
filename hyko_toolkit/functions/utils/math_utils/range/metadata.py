from hyko_sdk.models import CoreModel
from pydantic import Field

from hyko_toolkit.registry import ToolkitFunction

func = ToolkitFunction(name='range', task='math_utils', description='Generate a range of integers', absolute_dockerfile_path='./toolkit/hyko_toolkit/functions/utils/math_utils/Dockerfile', docker_context='./toolkit/hyko_toolkit/functions/utils/math_utils/range')

@func.set_param
class Params(CoreModel):
    start: int = Field(..., description='Start integer in the range')
    end: int = Field(..., description='End integer (not included in the range)')

@func.set_output
class Outputs(CoreModel):
    result: list[int] = Field(..., description='Output range')
