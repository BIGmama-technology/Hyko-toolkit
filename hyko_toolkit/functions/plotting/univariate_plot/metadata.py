from enum import Enum

from hyko_sdk.components.components import ListComponent, NumberField
from hyko_sdk.io import Image
from hyko_sdk.models import Category, CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.registry import ToolkitNode


class SupportedPlots(str, Enum):
    Pie_Chart = "Pie_Chart"
    Histogram = "Histogram"


func = ToolkitNode(
    category=Category.FUNCTION,
    name="univariate_plot",
    task="plotting",
    cost=2,
    description="Generate various types of plots with Y input.",
)


@func.set_input
class Inputs(CoreModel):
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
    image: Image = field(description="Output image.")
