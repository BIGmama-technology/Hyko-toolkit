from hyko_sdk.models import CoreModel
from pydantic import Field

from hyko_toolkit.registry import ToolkitFunction

func = ToolkitFunction(name='concat', task='text_utils', description='Concatenate two strings together', absolute_dockerfile_path='./toolkit/hyko_toolkit/functions/utils/text_utils/Dockerfile', docker_context='./toolkit/hyko_toolkit/functions/utils/text_utils/concat')

@func.set_input
class Inputs(CoreModel):
    first: str = Field(..., description='First string')
    second: str = Field(..., description='Second string')

@func.set_output
class Outputs(CoreModel):
    output: str = Field(..., description='Concatenated result')
