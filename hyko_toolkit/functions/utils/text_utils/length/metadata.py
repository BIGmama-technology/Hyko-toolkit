from hyko_sdk.models import CoreModel
from pydantic import Field

from hyko_toolkit.registry import ToolkitFunction

func = ToolkitFunction(name='length', task='text_utils', description='Calculate the length of a string', absolute_dockerfile_path='./toolkit/hyko_toolkit/functions/utils/text_utils/Dockerfile', docker_context='./toolkit/hyko_toolkit/functions/utils/text_utils/length')

@func.set_input
class Inputs(CoreModel):
    text: str = Field(..., description='Input text')

@func.set_output
class Outputs(CoreModel):
    length: int = Field(..., description='Length of the input string')
