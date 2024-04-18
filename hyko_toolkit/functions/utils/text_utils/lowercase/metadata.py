from hyko_sdk.models import CoreModel
from pydantic import Field

from hyko_toolkit.registry import ToolkitFunction

func = ToolkitFunction(name='lowercase', task='text_utils', description='Convert a given string to lowercase', absolute_dockerfile_path='./toolkit/hyko_toolkit/functions/utils/text_utils/Dockerfile', docker_context='./toolkit/hyko_toolkit/functions/utils/text_utils/lowercase')

@func.set_input
class Inputs(CoreModel):
    text: str = Field(..., description='Input text')

@func.set_output
class Outputs(CoreModel):
    lowercase_string: str = Field(..., description='Lowercase version of the input string')
