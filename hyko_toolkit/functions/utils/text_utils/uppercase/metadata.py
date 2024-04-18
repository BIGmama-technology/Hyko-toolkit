from hyko_sdk.models import CoreModel
from pydantic import Field

from hyko_toolkit.registry import ToolkitFunction

func = ToolkitFunction(name='uppercase', task='text_utils', description='Convert a given string to uppercase', absolute_dockerfile_path='./toolkit/hyko_toolkit/functions/utils/text_utils/Dockerfile', docker_context='./toolkit/hyko_toolkit/functions/utils/text_utils/uppercase')

@func.set_input
class Inputs(CoreModel):
    text: str = Field(..., description='Input text')

@func.set_output
class Outputs(CoreModel):
    uppercase_string: str = Field(..., description='Uppercase version of the input string')
