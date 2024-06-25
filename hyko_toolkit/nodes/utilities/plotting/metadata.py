from hyko_sdk.models import Tag

from hyko_toolkit.node_group import NodeGroup

from .bivariate_plot.metadata import node as bivariate_plot_node
from .univariate_plot.metadata import node as univariate_plot_node

node = NodeGroup(
    name="Plot utilities",
    description="perform various plotting tasks.",
    icon="image",
    tag=Tag.utilities,
    nodes=[bivariate_plot_node, univariate_plot_node],
)
