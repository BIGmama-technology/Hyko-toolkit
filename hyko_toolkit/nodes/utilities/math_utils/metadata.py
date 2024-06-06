from hyko_sdk.models import Tag

from hyko_toolkit.node_group import NodeGroup

from .arithmetic.metadata import node as arithmetic_node
from .random.metadata import node as random_node
from .range.metadata import node as range_node
from .round.metadata import node as round_node

node = NodeGroup(
    name="Math utilities",
    description="perform various mathematical operations.",
    icon="number",
    tag=Tag.utilities,
    nodes=[arithmetic_node, random_node, range_node, round_node],
)
