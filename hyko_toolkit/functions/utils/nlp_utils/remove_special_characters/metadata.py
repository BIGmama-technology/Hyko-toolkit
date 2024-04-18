from hyko_sdk.models import CoreModel
from pydantic import Field

from hyko_toolkit.registry import ToolkitFunction

func = ToolkitFunction(name='remove_special_characters', task='nlp_utils', description='A function to remove special characters and punctuation from text.', absolute_dockerfile_path='./toolkit/hyko_toolkit/functions/utils/nlp_utils/remove_special_characters/Dockerfile', docker_context='./toolkit/hyko_toolkit/functions/utils/nlp_utils/remove_special_characters')

@func.set_input
class Inputs(CoreModel):
    text: str = Field(..., description='The input text from which special characters and punctuation will be removed.')

@func.set_output
class Outputs(CoreModel):
    result: str = Field(..., description='The text with special characters and punctuation removed.')
