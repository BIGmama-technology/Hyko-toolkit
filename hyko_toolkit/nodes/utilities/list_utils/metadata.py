from hyko_sdk.models import Tag

from hyko_toolkit.node_group import NodeGroup

from .any.metadata import node as any_node
from .append.metadata import node as append_node
from .count.metadata import node as count_node
from .extend.metadata import node as extend_node
from .index.metadata import node as index_node
from .insert.metadata import node as insert_node
from .len.metadata import node as len_node
from .max.metadata import node as max_node
from .min.metadata import node as min_node
from .pop.metadata import node as pop_node
from .remove.metadata import node as remove_node
from .reverse.metadata import node as reverse_node
from .slice.metadata import node as slice_node
from .sort.metadata import node as sort_node
from .sum.metadata import node as sum_node

node = NodeGroup(
    name="List utilities",
    description="perform various list operations.",
    icon="list",
    tag=Tag.utilities,
    nodes=[
        any_node,
        append_node,
        count_node,
        extend_node,
        index_node,
        insert_node,
        len_node,
        max_node,
        min_node,
        pop_node,
        remove_node,
        reverse_node,
        slice_node,
        sort_node,
        sum_node,
    ],
)
