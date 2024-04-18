from enum import Enum

from hyko_sdk.models import CoreModel
from pydantic import Field

from hyko_toolkit.registry import ToolkitFunction

func = ToolkitFunction(name='replace', task='text_utils', description='Replace occurrences of a substring in a string', absolute_dockerfile_path='./toolkit/hyko_toolkit/functions/utils/text_utils/Dockerfile', docker_context='./toolkit/hyko_toolkit/functions/utils/text_utils/replace')

class ReplaceMode(str, Enum):
    replace_all = 'replaceAll'
    replace_first = 'replaceFirst'

@func.set_input
class Inputs(CoreModel):
    text: str = Field(..., description='Input text')

@func.set_param
class Params(CoreModel):
    old_substring: str = Field(..., description='Substring to replace')
    new_substring: str = Field(..., description='Replacement string')
    replace_mode: ReplaceMode = Field(default=ReplaceMode.replace_all, description='Replace mode: replaceAll or replaceFirst')

@func.set_output
class Outputs(CoreModel):
    replaced: str = Field(..., description='Text with replaced occurrences')
