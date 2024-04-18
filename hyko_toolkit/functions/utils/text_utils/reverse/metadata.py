from hyko_sdk.models import CoreModel
from pydantic import Field

from hyko_toolkit.registry import ToolkitFunction

func = ToolkitFunction(name='reverse', task='text_utils', description='Reverse a given string', absolute_dockerfile_path='./toolkit/hyko_toolkit/functions/utils/text_utils/Dockerfile', docker_context='./toolkit/hyko_toolkit/functions/utils/text_utils/reverse')

@func.set_input
class Inputs(CoreModel):
    text: str = Field(..., description='Input text')

@func.set_output
class Outputs(CoreModel):
    reversed: str = Field(..., description='Reversed input string')
