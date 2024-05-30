from enum import Enum

from hyko_sdk.components.components import ListComponent, NumberField
from hyko_sdk.io import Image
from hyko_sdk.models import Category, CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.registry import ToolkitNode


class SupportedPlots(str, Enum):
    Heatmaps = "Heatmap"
    Bar_Plot = "Bar_Plot"
    Line_Plot = "Line_Plot"
    Box_Plot = "Box_Plot"
    Area_Plot = "Area_Plot"
    Violin_Plot = "Violin_Plot"
    Pair_Plot = "Pair_Plot"
    Scatter_Plot = "Scatter_Plot"


func = ToolkitNode(
    name="Bivariate plot",
    task="Plotting",
    category=Category.FUNCTION,
    cost=2,
    description="Generate various types of plots with (X , Y) inputs.",
    icon="graph",
)


@func.set_input
class Inputs(CoreModel):
    x: list[float] = field(
        default=None,
        description="X",
        component=ListComponent(item_component=NumberField(placeholder="Enter X")),
    )
    y: list[float] = field(
        default=None,
        description="Y",
        component=ListComponent(item_component=NumberField(placeholder="Enter Y")),
    )


@func.set_param
class Params(CoreModel):
    plot_type: SupportedPlots = field(description="Select Plot Type.")


@func.set_output
class Outputs(CoreModel):
    image: Image = field(description="Output image")
