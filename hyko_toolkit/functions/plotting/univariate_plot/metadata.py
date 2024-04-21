from enum import Enum

from hyko_sdk.io import Image
from hyko_sdk.models import CoreModel
from pydantic import Field

from hyko_toolkit.registry import ToolkitFunction


class SupportedPlots(str, Enum):
    Pie_Chart = "Pie_Chart"
    Histogram = "Histogram"


func = ToolkitFunction(
    name="univariate_plot",
    task="plotting",
    description="Generate various types of plots with Y input.",
    absolute_dockerfile_path="./toolkit/hyko_toolkit/functions/plotting/Dockerfile",
    docker_context="./toolkit/hyko_toolkit/functions/plotting/univariate_plot",
)


@func.set_input
class Inputs(CoreModel):
    y: list[float] = Field(default=None, description="Y")


@func.set_param
class Params(CoreModel):
    plot_type: SupportedPlots = Field(..., description="Select Plot Type.")


@func.set_output
class Outputs(CoreModel):
    image: Image = Field(..., description="Output image.")
