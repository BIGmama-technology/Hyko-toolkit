from hyko_sdk.models import CoreModel
from pydantic import Field

from hyko_toolkit.registry import ToolkitFunction

func = ToolkitFunction(name='slice', task='text_utils', description='Create a slice of a given string of text', absolute_dockerfile_path='./toolkit/hyko_toolkit/functions/utils/text_utils/Dockerfile', docker_context='./toolkit/hyko_toolkit/functions/utils/text_utils/slice')

@func.set_input
class Inputs(CoreModel):
    text: str = Field(..., description='Text to be sliced')

@func.set_param
class Params(CoreModel):
    start: int = Field(default=None, description='Starting position for slicing')
    length: int = Field(default=None, description='Length of the slice')

@func.set_output
class Outputs(CoreModel):
    output_text: str = Field(..., description='Text slice result')
