from hyko_sdk.models import CoreModel
from pydantic import Field

from hyko_toolkit.registry import ToolkitFunction

func = ToolkitFunction(name='index_mapping', task='text_utils', description='Map indexes to strings and return the corresponding strings', absolute_dockerfile_path='./toolkit/hyko_toolkit/functions/utils/text_utils/Dockerfile', docker_context='./toolkit/hyko_toolkit/functions/utils/text_utils/index_mapping')

@func.set_input
class Inputs(CoreModel):
    input_strings: list[str] = Field(..., description='list of input strings')
    indexes: list[int] = Field(..., description='list of indexes')

@func.set_output
class Outputs(CoreModel):
    output_strings: list[str] = Field(..., description='list of mapped output strings')
