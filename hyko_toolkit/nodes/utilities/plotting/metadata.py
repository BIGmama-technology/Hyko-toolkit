from enum import Enum
from typing import Any

from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.models import CoreModel, MetaDataBase, Tag
from hyko_sdk.utils import field

from .bivariate_plot.metadata import func as bivariate_plot_node
from .univariate_plot.metadata import func as univariate_plot_node

node = ToolkitNode(
    name="Plot utilities",
    description="perform various plotting tasks.",
    icon="image",
    tag=Tag.utilities,
)


class PlotUtils(str, Enum):
    bivariate_plot = "bivariate_plot"
    univariate_plot = "univariate_plot"


@node.set_param
class Params(CoreModel):
    plot_util: PlotUtils = field(
        description="Type of the plot utility node, when this changes it updates the output port to correspond to it.",
    )


@node.callback(trigger="plot_util", id="change_plot_util")
async def change_plot_util_type(metadata: MetaDataBase, *_: Any):
    plot_util = metadata.params["plot_util"].value
    metadata.params = {}
    match plot_util:
        case PlotUtils.bivariate_plot.value:
            return bivariate_plot_node.get_metadata()
        case PlotUtils.univariate_plot.value:
            return univariate_plot_node.get_metadata()
        case _:
            return metadata
