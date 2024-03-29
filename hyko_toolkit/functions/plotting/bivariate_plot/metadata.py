from enum import Enum

from hyko_sdk.definitions import ToolkitFunction
from hyko_sdk.io import Image
from hyko_sdk.models import CoreModel
from pydantic import Field


class SupportedPlots(str, Enum):
    Heatmaps = "Heatmap"
    Bar_Plot = "Bar_Plot"
    Line_Plot = "Line_Plot"
    Box_Plot = "Box_Plot"
    Area_Plot = "Area_Plot"
    Violin_Plot = "Violin_Plot"
    Pair_Plot = "Pair_Plot"
    Scatter_Plot = "Scatter_Plot"


func = ToolkitFunction(
    name="bivariate_plot",
    task="plotting",
    description="Generate various types of plots with (X , Y) inputs.",
)


@func.set_input
class Inputs(CoreModel):
    x: list[float] = Field(default=None, description="X")
    y: list[float] = Field(default=None, description="Y")


@func.set_param
class Params(CoreModel):
    plot_type: SupportedPlots = Field(..., description="Select Plot Type.")


@func.set_output
class Outputs(CoreModel):
    image: Image = Field(..., description="Output image")
