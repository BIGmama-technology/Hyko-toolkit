from enum import Enum

from hyko_sdk.io import Image
from hyko_sdk.models import CoreModel
from pydantic import Field

from hyko_toolkit.registry import ToolkitFunction


class SupportedPlots(str, Enum):
    Heatmaps = 'Heatmap'
    Bar_Plot = 'Bar_Plot'
    Line_Plot = 'Line_Plot'
    Box_Plot = 'Box_Plot'
    Area_Plot = 'Area_Plot'
    Violin_Plot = 'Violin_Plot'
    Pair_Plot = 'Pair_Plot'
    Scatter_Plot = 'Scatter_Plot'
func = ToolkitFunction(name='bivariate_plot', task='plotting', description='Generate various types of plots with (X , Y) inputs.', absolute_dockerfile_path='./toolkit/hyko_toolkit/functions/plotting/Dockerfile', docker_context='./toolkit/hyko_toolkit/functions/plotting/bivariate_plot')

@func.set_input
class Inputs(CoreModel):
    x: list[float] = Field(default=None, description='X')
    y: list[float] = Field(default=None, description='Y')

@func.set_param
class Params(CoreModel):
    plot_type: SupportedPlots = Field(..., description='Select Plot Type.')

@func.set_output
class Outputs(CoreModel):
    image: Image = Field(..., description='Output image')
