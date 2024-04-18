from enum import Enum

from hyko_sdk.models import CoreModel
from pydantic import Field

from hyko_toolkit.registry import ToolkitFunction

func = ToolkitFunction(name='padding', task='text_utils', description='Pads text until it has a certain length', absolute_dockerfile_path='./toolkit/hyko_toolkit/functions/utils/text_utils/Dockerfile', docker_context='./toolkit/hyko_toolkit/functions/utils/text_utils/padding')

class PaddingAlignment(str, Enum):
    START = 'start'
    END = 'end'
    CENTER = 'center'

@func.set_input
class Inputs(CoreModel):
    text: str = Field(..., description='Text to be padded')

@func.set_param
class Params(CoreModel):
    width: int = Field(..., description='Width of the padded text')
    padding: str = Field(..., description='Padding character')
    alignment: PaddingAlignment = Field(default=PaddingAlignment.START, description='Padding alignment')

@func.set_output
class Outputs(CoreModel):
    output_text: str = Field(..., description='Padded text result')
