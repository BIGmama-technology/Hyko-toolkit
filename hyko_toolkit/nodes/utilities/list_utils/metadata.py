from hyko_sdk.models import Tag

from hyko_toolkit.node_group import NodeGroup

from .any.metadata import func as any_node
from .append.metadata import func as append_node
from .count.metadata import func as count_node
from .extend.metadata import func as extend_node
from .index.metadata import func as index_node
from .insert.metadata import func as insert_node
from .len.metadata import func as len_node
from .max.metadata import func as max_node
from .min.metadata import func as min_node
from .pop.metadata import func as pop_node
from .remove.metadata import func as remove_node
from .reverse.metadata import func as reverse_node
from .slice.metadata import func as slice_node
from .sort.metadata import func as sort_node
from .sum.metadata import func as sum_node

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
