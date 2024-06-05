from hyko_sdk.models import Tag

from hyko_toolkit.node_group import NodeGroup

from .arithmetic.metadata import func as arithmetic_node
from .random.metadata import func as random_node
from .range.metadata import func as range_node
from .round.metadata import func as round_node

node = NodeGroup(
    name="Math utilities",
    description="perform various mathematical operations.",
    icon="number",
    tag=Tag.utilities,
    nodes=[arithmetic_node, random_node, range_node, round_node],
)
