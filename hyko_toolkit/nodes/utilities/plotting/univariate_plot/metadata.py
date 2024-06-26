from enum import Enum

from hyko_sdk.components.components import ListComponent, NumberField
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.io import Image
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field


class SupportedPlots(str, Enum):
    Pie_Chart = "Pie_Chart"
    Histogram = "Histogram"


node = ToolkitNode(
    name="Univariate plot",
    cost=2,
    description="Generate various types of plots with Y input.",
    icon="graph",
    require_worker=True,
)


@node.set_input
class Inputs(CoreModel):
    y: list[float] = field(
        default=None,
        description="Y",
        component=ListComponent(item_component=NumberField(placeholder="Enter Y")),
    )


@node.set_param
class Params(CoreModel):
    plot_type: SupportedPlots = field(description="Select Plot Type.")


@node.set_output
class Outputs(CoreModel):
    image: Image = field(description="Output image.")
