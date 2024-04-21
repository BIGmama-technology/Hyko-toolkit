from hyko_sdk.models import CoreModel
from pydantic import Field

from hyko_toolkit.registry import ToolkitFunction

func = ToolkitFunction(
    name="random",
    task="math_utils",
    description="Generate a random integer",
    absolute_dockerfile_path="./toolkit/hyko_toolkit/functions/utils/math_utils/Dockerfile",
    docker_context="./toolkit/hyko_toolkit/functions/utils/math_utils/random",
)


@func.set_param
class Params(CoreModel):
    min_val: int = Field(..., description="Minimum value for random number generation")
    max_val: int = Field(..., description="Maximum value for random number generation")


@func.set_output
class Outputs(CoreModel):
    result: int = Field(..., description="Generated random number")
